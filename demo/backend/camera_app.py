from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import cv2
import numpy as np
from datetime import datetime
import time
import threading
import base64
from typing import List, Optional
from pydantic import BaseModel
import json

app = FastAPI(title="VisionQC Camera API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global değişkenler
camera = None
camera_lock = threading.Lock()
last_measurement = None
measurement_history: List[dict] = []
is_measuring = False

# Kalibrasyon değerleri (piksel/mm oranı)
CALIBRATION = {
    "pixels_per_mm": 10.0,  # Varsayılan, kalibre edilmeli
    "reference_width_mm": 85.6,  # Kredi kartı genişliği referans
    "reference_height_mm": 53.98  # Kredi kartı yüksekliği referans
}

# Ürün spesifikasyonları
PRODUCT_SPECS = {
    "FRC-180-STD": {
        "name": "Doku Forsepsi Standart",
        "nominal": {"length": 180.0, "width": 12.0},
        "tolerance": {"length": 1.0, "width": 0.3},
        "color_range": {"lower": [0, 0, 100], "upper": [180, 50, 255]}  # Metalik gri
    },
    "SCR-120-PRO": {
        "name": "Cerrahi Makas Pro",
        "nominal": {"length": 120.0, "width": 15.0},
        "tolerance": {"length": 0.8, "width": 0.4},
        "color_range": {"lower": [0, 0, 100], "upper": [180, 50, 255]}
    },
    "CUSTOM": {
        "name": "Özel Nesne",
        "nominal": {"length": 100.0, "width": 50.0},
        "tolerance": {"length": 5.0, "width": 2.5},
        "color_range": {"lower": [0, 0, 0], "upper": [180, 255, 255]}
    },
    "CARD-REF": {
        "name": "Kalibrasyon Kartı (Kredi Kartı)",
        "nominal": {"length": 85.6, "width": 53.98},
        "tolerance": {"length": 0.5, "width": 0.5},
        "color_range": {"lower": [0, 0, 0], "upper": [180, 255, 255]}
    }
}

class MeasurementResult(BaseModel):
    product_code: str
    product_name: str
    timestamp: str
    measurements: dict
    nominal: dict
    deviations: dict
    tolerance: dict
    status: str
    confidence: float
    processing_time_ms: float
    contour_area: float
    bounding_box: dict

def init_camera():
    """Kamerayı başlat"""
    global camera
    with camera_lock:
        if camera is None or not camera.isOpened():
            camera = cv2.VideoCapture(0)
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            camera.set(cv2.CAP_PROP_FPS, 30)
            time.sleep(0.5)  # Kamera ısınması için bekle
    return camera is not None and camera.isOpened()

def release_camera():
    """Kamerayı serbest bırak"""
    global camera
    with camera_lock:
        if camera is not None:
            camera.release()
            camera = None

def get_frame():
    """Kameradan tek kare al"""
    global camera
    with camera_lock:
        if camera is None or not camera.isOpened():
            return None
        ret, frame = camera.read()
        if ret:
            return frame
    return None

def detect_and_measure(frame, product_code="CUSTOM"):
    """Görüntüde nesne tespit et ve ölç"""
    start_time = time.time()
    
    spec = PRODUCT_SPECS.get(product_code, PRODUCT_SPECS["CUSTOM"])
    
    # Görüntü işleme
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Kenar tespiti
    edges = cv2.Canny(blurred, 50, 150)
    
    # Morfolojik işlemler
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)
    
    # Kontur bulma
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result = {
        "detected": False,
        "frame": frame.copy(),
        "measurements": None,
        "contours": []
    }
    
    if not contours:
        return result
    
    # En büyük konturu bul (min alan filtresi ile)
    min_area = 5000  # Minimum alan (gürültü filtresi)
    valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
    
    if not valid_contours:
        return result
    
    largest_contour = max(valid_contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)
    
    # Döndürülmüş minimum dikdörtgen
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    
    # Boyutları al (piksel)
    width_px = rect[1][0]
    height_px = rect[1][1]
    
    # Uzun kenar = length, kısa kenar = width
    if width_px < height_px:
        width_px, height_px = height_px, width_px
    
    # Piksel → mm dönüşümü
    ppm = CALIBRATION["pixels_per_mm"]
    length_mm = width_px / ppm
    width_mm = height_px / ppm
    
    # Nominal değerlerle karşılaştır
    nominal = spec["nominal"]
    tolerance = spec["tolerance"]
    
    length_dev = length_mm - nominal["length"]
    width_dev = width_mm - nominal["width"]
    
    # Durum belirleme
    status = "PASSED"
    if abs(length_dev) > tolerance["length"] or abs(width_dev) > tolerance["width"]:
        status = "FAILED"
    
    # Güven skoru (kontur kalitesine göre)
    perimeter = cv2.arcLength(largest_contour, True)
    circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
    confidence = min(95 + circularity * 5, 99.9)
    
    # Sonuç görüntüsü oluştur
    result_frame = frame.copy()
    
    # Kontur çiz
    color = (0, 255, 0) if status == "PASSED" else (0, 0, 255)
    cv2.drawContours(result_frame, [box], 0, color, 3)
    
    # Merkez noktası
    center = (int(rect[0][0]), int(rect[0][1]))
    cv2.circle(result_frame, center, 5, color, -1)
    
    # Ölçüm bilgilerini yaz
    cv2.putText(result_frame, f"L: {length_mm:.1f}mm", (center[0] - 60, center[1] - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(result_frame, f"W: {width_mm:.1f}mm", (center[0] - 60, center[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # Durum etiketi
    label = "GECTI" if status == "PASSED" else "KALDI"
    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
    cv2.rectangle(result_frame, (10, 10), (20 + label_size[0], 60), color, -1)
    cv2.putText(result_frame, label, (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    
    # Kalibrasyon bilgisi
    cv2.putText(result_frame, f"PPM: {ppm:.1f}", (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    processing_time = (time.time() - start_time) * 1000
    
    result = {
        "detected": True,
        "frame": result_frame,
        "measurements": {
            "product_code": product_code,
            "product_name": spec["name"],
            "timestamp": datetime.now().isoformat(),
            "measurements": {"length": round(length_mm, 2), "width": round(width_mm, 2)},
            "nominal": nominal,
            "deviations": {"length": round(length_dev, 2), "width": round(width_dev, 2)},
            "tolerance": tolerance,
            "status": status,
            "confidence": round(confidence, 1),
            "processing_time_ms": round(processing_time, 1),
            "contour_area": round(area, 0),
            "bounding_box": {
                "center_x": center[0],
                "center_y": center[1],
                "width_px": round(width_px, 1),
                "height_px": round(height_px, 1),
                "angle": round(rect[2], 1)
            }
        },
        "contours": [box.tolist()]
    }
    
    return result

def generate_video_stream():
    """Video stream generator"""
    global last_measurement, is_measuring
    
    if not init_camera():
        return
    
    while True:
        frame = get_frame()
        if frame is None:
            continue
        
        # Eğer ölçüm modu aktifse, tespit ve ölçüm yap
        if is_measuring:
            result = detect_and_measure(frame, "CUSTOM")
            if result["detected"]:
                frame = result["frame"]
                last_measurement = result["measurements"]
        else:
            # Sadece kenar tespiti göster (önizleme)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
            
            # Konturları bul ve çiz
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            valid_contours = [c for c in contours if cv2.contourArea(c) > 5000]
            cv2.drawContours(frame, valid_contours, -1, (0, 255, 255), 2)
            
            # Önizleme modu etiketi
            cv2.putText(frame, "ONIZLEME", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # JPEG olarak encode et
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS

@app.on_event("startup")
async def startup():
    init_camera()

@app.on_event("shutdown")
async def shutdown():
    release_camera()

@app.get("/")
async def root():
    return {"message": "VisionQC Camera API - Gerçek Zamanlı Kalite Kontrol"}

@app.get("/video_feed")
async def video_feed():
    """Canlı video stream"""
    return StreamingResponse(
        generate_video_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/camera/status")
async def camera_status():
    """Kamera durumunu kontrol et"""
    global camera
    is_open = camera is not None and camera.isOpened()
    return {"camera_available": is_open}

@app.post("/camera/init")
async def init_cam():
    """Kamerayı başlat"""
    success = init_camera()
    return {"success": success}

@app.post("/camera/release")
async def release_cam():
    """Kamerayı serbest bırak"""
    release_camera()
    return {"success": True}

@app.post("/measure/start")
async def start_measuring():
    """Ölçüm modunu başlat"""
    global is_measuring
    is_measuring = True
    return {"measuring": True}

@app.post("/measure/stop")
async def stop_measuring():
    """Ölçüm modunu durdur"""
    global is_measuring
    is_measuring = False
    return {"measuring": False}

@app.post("/measure/capture")
async def capture_and_measure(product_code: str = "CUSTOM"):
    """Tek kare yakala ve ölç"""
    global last_measurement, measurement_history
    
    frame = get_frame()
    if frame is None:
        raise HTTPException(status_code=500, detail="Kamera görüntüsü alınamadı")
    
    result = detect_and_measure(frame, product_code)
    
    if not result["detected"]:
        raise HTTPException(status_code=404, detail="Nesne tespit edilemedi")
    
    # Görüntüyü base64'e çevir
    _, buffer = cv2.imencode('.jpg', result["frame"])
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    measurement = result["measurements"]
    measurement["image"] = img_base64
    
    # Geçmişe ekle
    measurement_history.insert(0, {k: v for k, v in measurement.items() if k != "image"})
    if len(measurement_history) > 100:
        measurement_history.pop()
    
    last_measurement = measurement
    
    return measurement

@app.get("/measure/last")
async def get_last_measurement():
    """Son ölçümü getir"""
    if last_measurement is None:
        raise HTTPException(status_code=404, detail="Henüz ölçüm yapılmadı")
    return last_measurement

@app.post("/calibrate")
async def calibrate(reference_length_mm: float = 85.6, reference_width_mm: float = 53.98):
    """
    Kalibre et - Bilinen boyutlarda bir referans nesne kullanarak.
    Varsayılan: Kredi kartı (85.6mm x 53.98mm)
    """
    global CALIBRATION
    
    frame = get_frame()
    if frame is None:
        raise HTTPException(status_code=500, detail="Kamera görüntüsü alınamadı")
    
    result = detect_and_measure(frame, "CARD-REF")
    
    if not result["detected"]:
        raise HTTPException(status_code=404, detail="Referans nesne tespit edilemedi")
    
    # Piksel boyutlarını al
    bbox = result["measurements"]["bounding_box"]
    width_px = bbox["width_px"]
    height_px = bbox["height_px"]
    
    # Yeni PPM hesapla (ortalama)
    ppm_length = width_px / reference_length_mm
    ppm_width = height_px / reference_width_mm
    new_ppm = (ppm_length + ppm_width) / 2
    
    CALIBRATION["pixels_per_mm"] = new_ppm
    CALIBRATION["reference_width_mm"] = reference_length_mm
    CALIBRATION["reference_height_mm"] = reference_width_mm
    
    return {
        "success": True,
        "pixels_per_mm": round(new_ppm, 2),
        "measured_px": {"width": width_px, "height": height_px},
        "reference_mm": {"length": reference_length_mm, "width": reference_width_mm}
    }

@app.get("/calibration")
async def get_calibration():
    """Kalibrasyon değerlerini getir"""
    return CALIBRATION

@app.post("/calibration/set")
async def set_calibration(pixels_per_mm: float):
    """Manuel kalibrasyon değeri ayarla"""
    global CALIBRATION
    CALIBRATION["pixels_per_mm"] = pixels_per_mm
    return {"success": True, "pixels_per_mm": pixels_per_mm}

@app.get("/products")
async def get_products():
    """Ürün listesini getir"""
    return [{"code": k, "name": v["name"], "nominal": v["nominal"], "tolerance": v["tolerance"]} 
            for k, v in PRODUCT_SPECS.items()]

@app.get("/history")
async def get_history(limit: int = 50):
    """Ölçüm geçmişini getir"""
    return measurement_history[:limit]

@app.get("/dashboard")
async def get_dashboard():
    """Dashboard istatistikleri"""
    total = len(measurement_history)
    passed = sum(1 for m in measurement_history if m["status"] == "PASSED")
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0
    avg_time = sum(m["processing_time_ms"] for m in measurement_history) / total if total > 0 else 0
    
    return {
        "total_inspections": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(pass_rate, 1),
        "avg_processing_time": round(avg_time, 1),
        "calibration": CALIBRATION,
        "recent_inspections": measurement_history[:20]
    }

@app.delete("/history")
async def clear_history():
    """Geçmişi temizle"""
    measurement_history.clear()
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
