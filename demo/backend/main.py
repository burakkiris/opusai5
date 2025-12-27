from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import random

app = FastAPI(title="VisionQC API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ürün spesifikasyonları veritabanı (Cerrahi Aletler)
PRODUCT_SPECS = {
    "FRC-180-STD": {
        "name": "Doku Forsepsi Standart",
        "nominal": {"length": 180.0, "width": 12.0, "height": 8.0},
        "tolerance": {"length": 1.0, "width": 0.3, "height": 0.2},
        "unit": "mm"
    },
    "SCR-120-PRO": {
        "name": "Cerrahi Makas Pro",
        "nominal": {"length": 120.0, "width": 15.0, "height": 6.0},
        "tolerance": {"length": 0.8, "width": 0.4, "height": 0.3},
        "unit": "mm"
    },
    "CLM-090-ECO": {
        "name": "Klemp Ekonomik",
        "nominal": {"length": 90.0, "width": 8.0, "height": 5.0},
        "tolerance": {"length": 0.5, "width": 0.2, "height": 0.15},
        "unit": "mm"
    },
    "RTR-150-MED": {
        "name": "Retraktör Medikal",
        "nominal": {"length": 150.0, "width": 20.0, "height": 10.0},
        "tolerance": {"length": 1.2, "width": 0.5, "height": 0.4},
        "unit": "mm"
    },
    "NHD-080-PRE": {
        "name": "İğne Tutucu Presizyon",
        "nominal": {"length": 80.0, "width": 6.0, "height": 4.0},
        "tolerance": {"length": 0.3, "width": 0.15, "height": 0.1},
        "unit": "mm"
    }
}

# Geçmiş kontrol kayıtları
measurement_history: List[dict] = []

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
    issues: List[str]

class DashboardStats(BaseModel):
    total_inspections: int
    passed: int
    failed: int
    pass_rate: float
    avg_processing_time: float
    recent_inspections: List[dict]

def simulate_measurement(product_code: str) -> dict:
    """Ölçüm simülasyonu - demo için"""
    start_time = datetime.now()
    
    spec = PRODUCT_SPECS.get(product_code)
    if not spec:
        raise ValueError(f"Ürün bulunamadı: {product_code}")
    
    nominal = spec["nominal"]
    tolerance = spec["tolerance"]
    
    # Gerçekçi ölçüm simülasyonu
    # %88 ihtimalle tolerans içinde, %12 ihtimalle tolerans dışı
    is_defective = random.random() < 0.12
    
    measurements = {}
    deviations = {}
    issues = []
    
    for dim in ["length", "width", "height"]:
        nom = nominal[dim]
        tol = tolerance[dim]
        
        if is_defective and random.random() < 0.5:
            deviation = random.uniform(tol * 1.1, tol * 2.0) * random.choice([-1, 1])
            label = "Uzunluk" if dim == "length" else "Genişlik" if dim == "width" else "Yükseklik"
            issues.append(f"{label} tolerans aşımı: {abs(deviation):.2f}mm sapma")
        else:
            deviation = random.uniform(-tol * 0.8, tol * 0.8)
        
        measured = nom + deviation
        measurements[dim] = round(measured, 2)
        deviations[dim] = round(deviation, 2)
    
    status = "PASSED"
    for dim in ["length", "width", "height"]:
        if abs(deviations[dim]) > tolerance[dim]:
            status = "FAILED"
            break
    
    confidence = random.uniform(96.5, 99.8) if status == "PASSED" else random.uniform(94.0, 98.5)
    processing_time = (datetime.now() - start_time).total_seconds() * 1000 + random.uniform(150, 300)
    
    return {
        "measurements": measurements,
        "deviations": deviations,
        "status": status,
        "confidence": round(confidence, 1),
        "processing_time_ms": round(processing_time, 1),
        "issues": issues
    }

@app.get("/")
async def root():
    return {"message": "VisionQC API - Yapay Zeka Destekli Kalite Kontrol Sistemi"}

@app.get("/products")
async def get_products():
    """Tüm ürün listesini döndür"""
    products = []
    for code, spec in PRODUCT_SPECS.items():
        products.append({
            "code": code,
            "name": spec["name"],
            "nominal": spec["nominal"],
            "tolerance": spec["tolerance"]
        })
    return products

@app.get("/products/{product_code}")
async def get_product(product_code: str):
    """Belirli bir ürünün spesifikasyonlarını döndür"""
    if product_code not in PRODUCT_SPECS:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    spec = PRODUCT_SPECS[product_code]
    return {
        "code": product_code,
        "name": spec["name"],
        "nominal": spec["nominal"],
        "tolerance": spec["tolerance"],
        "unit": spec["unit"]
    }

@app.post("/simulate")
async def simulate(product_code: str):
    """Demo için simüle edilmiş kontrol (görüntü olmadan)"""
    if product_code not in PRODUCT_SPECS:
        raise HTTPException(status_code=400, detail="Geçersiz ürün kodu")
    
    spec = PRODUCT_SPECS[product_code]
    nominal = spec["nominal"]
    tolerance = spec["tolerance"]
    
    is_defective = random.random() < 0.12
    
    measurements = {}
    deviations = {}
    issues = []
    
    for dim in ["length", "width", "height"]:
        nom = nominal[dim]
        tol = tolerance[dim]
        
        if is_defective and random.random() < 0.5:
            deviation = random.uniform(tol * 1.1, tol * 1.8) * random.choice([-1, 1])
            issues.append(f"{dim.capitalize()} tolerans aşımı: {abs(deviation):.2f}mm sapma")
        else:
            deviation = random.uniform(-tol * 0.85, tol * 0.85)
        
        measured = nom + deviation
        measurements[dim] = round(measured, 2)
        deviations[dim] = round(deviation, 2)
    
    status = "PASSED"
    for dim in ["length", "width", "height"]:
        if abs(deviations[dim]) > tolerance[dim]:
            status = "FAILED"
            break
    
    confidence = random.uniform(96.5, 99.8) if status == "PASSED" else random.uniform(94.0, 98.5)
    processing_time = random.uniform(180, 320)
    
    measurement_record = {
        "product_code": product_code,
        "product_name": spec["name"],
        "timestamp": datetime.now().isoformat(),
        "measurements": measurements,
        "nominal": nominal,
        "deviations": deviations,
        "tolerance": tolerance,
        "status": status,
        "confidence": round(confidence, 1),
        "processing_time_ms": round(processing_time, 1),
        "issues": issues
    }
    
    measurement_history.insert(0, measurement_record)
    if len(measurement_history) > 100:
        measurement_history.pop()
    
    return measurement_record

@app.get("/dashboard")
async def get_dashboard():
    """Dashboard istatistiklerini döndür"""
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
        "recent_inspections": measurement_history[:20]
    }

@app.get("/history")
async def get_history(limit: int = 50):
    """Kontrol geçmişini döndür"""
    return measurement_history[:limit]

@app.delete("/history")
async def clear_history():
    """Geçmişi temizle"""
    measurement_history.clear()
    return {"message": "Geçmiş temizlendi"}

@app.post("/batch-simulate")
async def batch_simulate(count: int = 20):
    """Toplu simülasyon - demo için hızlı veri üretimi"""
    results = []
    product_codes = list(PRODUCT_SPECS.keys())
    
    for _ in range(count):
        product_code = random.choice(product_codes)
        spec = PRODUCT_SPECS[product_code]
        nominal = spec["nominal"]
        tolerance = spec["tolerance"]
        
        is_defective = random.random() < 0.08
        
        measurements = {}
        deviations = {}
        issues = []
        
        for dim in ["length", "width", "height"]:
            nom = nominal[dim]
            tol = tolerance[dim]
            
            if is_defective and random.random() < 0.6:
                deviation = random.uniform(tol * 1.05, tol * 1.5) * random.choice([-1, 1])
                issues.append(f"{dim.capitalize()} tolerans aşımı")
            else:
                deviation = random.uniform(-tol * 0.9, tol * 0.9)
            
            measurements[dim] = round(nom + deviation, 2)
            deviations[dim] = round(deviation, 2)
        
        status = "PASSED"
        for dim in ["length", "width", "height"]:
            if abs(deviations[dim]) > tolerance[dim]:
                status = "FAILED"
                break
        
        record = {
            "product_code": product_code,
            "product_name": spec["name"],
            "timestamp": datetime.now().isoformat(),
            "measurements": measurements,
            "nominal": nominal,
            "deviations": deviations,
            "tolerance": tolerance,
            "status": status,
            "confidence": round(random.uniform(95, 99.5), 1),
            "processing_time_ms": round(random.uniform(150, 350), 1),
            "issues": issues
        }
        
        measurement_history.insert(0, record)
        results.append(record)
    
    if len(measurement_history) > 100:
        measurement_history[:] = measurement_history[:100]
    
    return {"generated": len(results), "results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
