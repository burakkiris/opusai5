# OpusAi5 - Proje Teknik Raporu

## 📋 Proje Özeti

**Proje Adı:** OpusAi5 - Cerrahi Aletlere Yönelik Hibrit Yapay Zeka Tabanlı Görsel Kalite Kontrol Sistemi  
**Kurum:** Aygün Cerrahi Aletler  
**Problem:** Problem 2 – Yüzey Parlaklığı ve Eloksal Renk Uyumsuzluğu  
**Amaç:** Görsel kalite standardının sağlanması

---

## 🎯 Problem Tanımı

Cerrahi aletlerin eloksal kaplama sürecinde karşılaşılan sorunlar:
- **Renk tutarsızlığı:** Aynı üründe farklı tonlar
- **Parlaklık değişkenliği:** Yüzey parlaklığında homojenlik eksikliği
- **Yüzey pürüzlülüğü:** Pürüzsüz olması gereken yüzeylerde düzensizlikler

---

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐     HTTP/REST      ┌──────────────────┐
│   Frontend      │ ◄─────────────────► │    Backend       │
│   (HTML/JS)     │                     │    (FastAPI)     │
│   Port: 3001    │                     │    Port: 8001    │
└─────────────────┘                     └──────────────────┘
                                               │
                                               ▼
                                        ┌──────────────────┐
                                        │  OpenCV + NumPy  │
                                        │  Görüntü İşleme  │
                                        └──────────────────┘
```

---

## 📦 Kullanılan Teknolojiler

| Katman | Teknoloji | Versiyon |
|--------|-----------|----------|
| Backend | Python | 3.9+ |
| Web Framework | FastAPI | 0.100+ |
| Görüntü İşleme | OpenCV | 4.8+ |
| Sayısal Hesaplama | NumPy | 1.24+ |
| Frontend | HTML5/CSS3/JavaScript | - |
| UI Framework | TailwindCSS | 3.x |
| Grafikler | Chart.js | 4.x |

---

## 🎨 Renk Standartları (AYGUN_COLOR_STANDARDS)

Aygün Cerrahi Aletler için tanımlı renk standartları:

| Renk Kodu | RAL | L* | a* | b* | RGB | Tolerans (Premium) |
|-----------|-----|----|----|----|----|-------------------|
| MAVI | 5015 | 45.5 | -8.2 | -32.5 | (0, 102, 178) | 1.5 ΔE |
| YEŞİL | 6024 | 52.3 | -45.2 | 28.5 | (0, 153, 76) | 1.5 ΔE |
| KIRMIZI | 3020 | 42.5 | 55.2 | 38.5 | (204, 51, 51) | 1.5 ΔE |
| SARI | 1023 | 85.2 | -2.5 | 75.5 | (255, 204, 0) | 1.5 ΔE |
| SİYAH | 7042 | 35.5 | 0.5 | -1.2 | (140, 140, 140) | 2.0 ΔE |

**Tolerans Seviyeleri:**
- **Premium:** ΔE ≤ 1.5 (kritik tıbbi cihazlar)
- **Standard:** ΔE ≤ 2.5 (standart ürünler)
- **Functional:** ΔE ≤ 4.0 (fonksiyonel parçalar)

---

## 🔬 Ölçüm Parametreleri ve Fonksiyonlar

### 1. Renk Analizi (Delta E 2000)

**Fonksiyon:** `calculate_delta_e_2000(lab1, lab2)`

**Açıklama:** CIEDE2000 standardına göre iki renk arasındaki algısal farkı hesaplar.

**Formül:**
```
ΔE₀₀ = √[(ΔL'/kₗSₗ)² + (ΔC'/kᴄSᴄ)² + (ΔH'/kₕSₕ)² + Rₜ(ΔC'/kᴄSᴄ)(ΔH'/kₕSₕ)]
```

**Kod:**
```python
def calculate_delta_e_2000(lab1, lab2):
    L1, a1, b1 = lab1["L"], lab1["a"], lab1["b"]
    L2, a2, b2 = lab2["L"], lab2["a"], lab2["b"]
    
    dL = L2 - L1
    da = a2 - a1
    db = b2 - b1
    
    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)
    dC = C2 - C1
    
    dH_sq = da**2 + db**2 - dC**2
    dH = math.sqrt(max(0, dH_sq))
    
    SL = 1
    SC = 1 + 0.045 * (C1 + C2) / 2
    SH = 1 + 0.015 * (C1 + C2) / 2
    
    delta_e = math.sqrt((dL/SL)**2 + (dC/SC)**2 + (dH/SH)**2)
    return round(delta_e, 2)
```

**Çıktı Yorumlama:**
| ΔE Değeri | Anlam |
|-----------|-------|
| 0 - 1.0 | Fark algılanamaz |
| 1.0 - 2.0 | Yakın incelemeyle fark edilir |
| 2.0 - 3.5 | Orta seviye fark |
| 3.5 - 5.0 | Belirgin fark |
| > 5.0 | Farklı renk olarak algılanır |

---

### 2. RGB → CIE L*a*b* Dönüşümü

**Fonksiyon:** `rgb_to_lab(rgb)`

**Açıklama:** RGB renk değerlerini CIE L*a*b* renk uzayına dönüştürür.

**Dönüşüm Adımları:**
1. RGB → Linear RGB (gamma düzeltme)
2. Linear RGB → XYZ (matris çarpımı)
3. XYZ → L*a*b* (D65 referans beyaz)

**Kod:**
```python
def rgb_to_lab(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    
    # Gamma düzeltme
    r = ((r + 0.055) / 1.055) ** 2.4 if r > 0.04045 else r / 12.92
    g = ((g + 0.055) / 1.055) ** 2.4 if g > 0.04045 else g / 12.92
    b = ((b + 0.055) / 1.055) ** 2.4 if b > 0.04045 else b / 12.92
    
    r, g, b = r * 100, g * 100, b * 100
    
    # RGB → XYZ
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    
    # XYZ → Lab (D65)
    x, y, z = x / 95.047, y / 100.0, z / 108.883
    
    x = x ** (1/3) if x > 0.008856 else (7.787 * x) + (16/116)
    y = y ** (1/3) if y > 0.008856 else (7.787 * y) + (16/116)
    z = z ** (1/3) if z > 0.008856 else (7.787 * z) + (16/116)
    
    L = (116 * y) - 16
    a = 500 * (x - y)
    b_val = 200 * (y - z)
    
    return {"L": round(L, 2), "a": round(a, 2), "b": round(b_val, 2)}
```

---

### 3. Parlaklık (Gloss) Hesaplama

**Fonksiyon:** `calculate_gloss(image)`

**Açıklama:** Görüntüden yüzey parlaklığını tahmin eder (0-100 GU).

**Yöntem:** Histogram analizi - yüksek yoğunluklu piksellerin oranı

**Kod:**
```python
def calculate_gloss(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    
    high_values = np.sum(hist[200:256])
    total = np.sum(hist)
    
    gloss = (high_values / total) * 100 * 1.5
    gloss = min(100, max(0, gloss))
    
    std = np.std(gray)
    gloss = (gloss + std / 2.55) / 2
    
    return round(gloss, 1)
```

**Parlaklık Sınıfları:**
| GU Değeri | Sınıf |
|-----------|-------|
| > 70 | Yüksek Parlaklık |
| 40 - 70 | Orta Parlaklık |
| 20 - 40 | Düşük Parlaklık |
| < 20 | Mat |

---

### 4. Yüzey Kalite Analizi

**Fonksiyon:** `analyze_surface_quality(image)`

**Bileşenler:**

#### a) Parlaklık Sınıflandırma
```python
if gloss >= 70: gloss_class = "YÜKSEK PARLAKLIK"
elif gloss >= 40: gloss_class = "ORTA PARLAKLIK"
elif gloss >= 20: gloss_class = "DÜŞÜK PARLAKLIK"
else: gloss_class = "MAT"
```

#### b) Yüzey Pürüzlülüğü (Ra) Tahmini
```python
laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
gradient_magnitude = np.sqrt(sobelx**2 + sobely**2).mean()

roughness_ra = (laplacian_var * 0.001 + gradient_magnitude * 0.005)
```

**Pürüzlülük Sınıfları:**
| Ra (μm) | Sınıf |
|---------|-------|
| < 0.2 | Çok Pürüzsüz |
| 0.2 - 0.4 | Pürüzsüz |
| 0.4 - 0.8 | Normal |
| 0.8 - 1.6 | Pürüzlü |
| > 1.6 | Çok Pürüzlü |

#### c) Yüzey Homojenliği
```python
# Görüntüyü bloklara böl ve her bloğun varyansını hesapla
blocks = [image[i:i+block_size, j:j+block_size] 
          for i in range(0, h, block_size) 
          for j in range(0, w, block_size)]
variances = [np.var(block) for block in blocks]
uniformity_score = 100 - min(100, np.std(variances) / 10)
```

#### d) Kalite Sınıfı
```python
surface_score = (gloss_normalized * 0.3 + 
                 roughness_normalized * 0.4 + 
                 uniformity_score * 0.3)

if surface_score >= 90: quality_grade = "A+"
elif surface_score >= 80: quality_grade = "A"
elif surface_score >= 70: quality_grade = "B"
elif surface_score >= 60: quality_grade = "C"
else: quality_grade = "D"
```

---

### 5. Renk Tutarlılık Analizi

**Fonksiyon:** `analyze_color_consistency(image, color_code)`

**Açıklama:** Görüntüyü bölgelere ayırıp her bölgedeki renk sapmasını analiz eder.

**Yöntem:**
```python
# Görüntüyü 3x3 grid'e böl
zones = []
for i in range(3):
    for j in range(3):
        zone = image[i*zone_h:(i+1)*zone_h, j*zone_w:(j+1)*zone_w]
        zone_lab = rgb_to_lab(np.mean(zone, axis=(0,1)))
        zone_delta_e = calculate_delta_e_2000(zone_lab, ref_lab)
        zones.append(zone_delta_e)

# Tutarlılık skoru
consistency = 100 - (np.std(zones) * 10 + np.mean(zones) * 5)
```

---

### 6. Kusur Tespiti

**Fonksiyon:** `detect_surface_defects(image)`

**Yöntem:** Adaptif eşikleme + kontur analizi

**Kod:**
```python
def detect_surface_defects(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh = cv2.adaptiveThreshold(
        blurred, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    defects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if 100 < area < 5000:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            if aspect_ratio > 3:
                defect_type = "CIZIK"
            elif area < 500:
                defect_type = "LEKE"
            else:
                defect_type = "DALGA"
            
            defects.append({
                "type": defect_type,
                "location": {"x": x, "y": y, "w": w, "h": h},
                "area": area
            })
    
    return defects[:5]
```

**Kusur Tipleri:**
| Tip | Açıklama | Önem |
|-----|----------|------|
| ÇİZİK | Uzun, ince kusurlar | Kritik |
| LEKE | Küçük noktasal kusurlar | Orta |
| DALGA | Yüzey dalgalanması | Kritik |

---

### 7. Isı Haritası Oluşturma

**Fonksiyon:** `generate_color_heatmap(image, color_code)`

**Açıklama:** Renk sapma haritası - her pikseldeki Delta E değerini görselleştirir.

**Renk Kodlaması:**
- 🟢 Yeşil: ΔE < 1 (Mükemmel)
- 🟡 Sarı: 1 ≤ ΔE < 3 (Kabul edilebilir)
- 🔴 Kırmızı: ΔE ≥ 3 (Problem)

---

## 📊 API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/analyze/upload` | POST | Görsel yükle ve analiz et |
| `/analyze` | POST | Kamera görüntüsünü analiz et |
| `/video_feed` | GET | Canlı kamera stream |
| `/heatmap_feed` | GET | Canlı ısı haritası stream |
| `/color-standards` | GET | Renk standartlarını getir |
| `/products` | GET | Ürün listesi |
| `/dashboard` | GET | İstatistik özeti |

---

## 📈 Çıktı Parametreleri

Analiz sonucunda dönen veriler:

```json
{
    "product_code": "AYG-STR-001",
    "product_name": "Sterilizasyon Konteyneri",
    "measured_lab": {"L": 45.2, "a": -8.1, "b": -32.3},
    "reference_lab": {"L": 45.5, "a": -8.2, "b": -32.5},
    "delta_e": 0.42,
    "delta_e_status": "UYGUN",
    "overall_status": "ONAY",
    "confidence": 94.2,
    "gloss_value": 65.3,
    "defect_count": 0,
    "surface_quality": {
        "gloss_class": "ORTA PARLAKLIK",
        "roughness_ra": 0.35,
        "roughness_class": "PÜRÜZSÜZ",
        "surface_score": 85,
        "quality_grade": "A"
    },
    "color_consistency": {
        "consistency_score": 92,
        "recommendation": "Renk tutarlılığı iyi seviyede"
    }
}
```

---

## 🔄 Karar Mekanizması

```
                    ┌─────────────────┐
                    │  Görüntü Analizi │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
    ┌───────────┐    ┌───────────┐    ┌───────────┐
    │ Renk (ΔE) │    │ Parlaklık │    │  Kusurlar │
    └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
          │                │                │
          ▼                ▼                ▼
    ΔE ≤ Tolerans?   GU Aralıkta?    Kritik Kusur?
          │                │                │
          └────────────────┼────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
         Tümü UYGUN               Herhangi biri UYGUNSUZ
              │                         │
              ▼                         ▼
           ✅ ONAY                   ❌ RED / ⚠️ İNCELEME
```

---

## 📁 Dosya Yapısı

```
demo2/
├── app.html              # Ana uygulama arayüzü
├── index.html            # Giriş sayfası
├── colorqc.html          # Alternatif arayüz
├── PROJE_RAPORU.md       # Bu döküman
└── backend/
    ├── color_qc.py       # Ana backend kodu
    ├── requirements.txt  # Python bağımlılıkları
    └── venv/             # Sanal ortam
```

---

## 🚀 Kurulum ve Çalıştırma

```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
python color_qc.py

# Frontend
# Port 3001'de serve edin (Live Server vb.)
```

---

## 📌 Gelecek Geliştirmeler

1. **Derin Öğrenme Modeli:** YOLOv8 ile kusur tespiti
2. **Spektrofotometre Entegrasyonu:** Gerçek renk ölçümü
3. **Veritabanı:** Ölçüm geçmişi kayıt
4. **Raporlama:** PDF rapor oluşturma
5. **SPC Modülü:** İstatistiksel Proses Kontrol

---

## 👥 Ekip

**Proje:** Yapay Zeka ile Dönüşüm Yarışması  
**Kurum:** Aygün Cerrahi Aletler

---

*Son Güncelleme: Aralık 2024*
