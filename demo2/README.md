# OpusAi5 - Cerrahi Aletlere Yönelik Hibrit Yapay Zeka Tabanlı Görsel Kalite Kontrol Sistemi

## 🚀 Projeyi Başlatma

### Gereksinimler
- Python 3.9+
- Node.js (frontend için) veya Live Server
- Tarayıcı (Chrome/Firefox önerilir)

---

## 📦 Kurulum

### 1. Backend Kurulumu

```bash
# Proje dizinine git
cd demo2/backend

# Virtual environment oluştur (ilk kurulumda)
python3 -m venv venv

# Virtual environment'ı aktifleştir
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

---

## ▶️ Projeyi Çalıştırma

### Backend'i Başlat

```bash
# Backend dizinine git
cd demo2/backend

# Virtual environment'ı aktifleştir
source venv/bin/activate

# Sunucuyu başlat
python3 color_qc.py
```

✅ Backend çalışıyor: `http://localhost:8001`

---

### Frontend'i Başlat

**Seçenek 1: Live Server (VSCode)**
1. `app.html` dosyasına sağ tıkla
2. "Open with Live Server" seç
3. Tarayıcıda otomatik açılır: `http://localhost:3001`

**Seçenek 2: Python HTTP Server**
```bash
# demo2 dizinine git
cd demo2

# HTTP sunucu başlat
python3 -m http.server 3001
```

✅ Frontend çalışıyor: `http://localhost:3001/app.html`

---

## 🎯 Hızlı Başlangıç (Tek Komut)

### Terminal 1 - Backend
```bash
cd demo2/backend && source venv/bin/activate && python3 color_qc.py
```

### Terminal 2 - Frontend
```bash
cd demo2 && python3 -m http.server 3001
```

Tarayıcıda aç: `http://localhost:3001/app.html`

---

## 🧪 Test Etme

1. **Demo Analiz:**
   - "Demo" butonuna tıkla
   - Otomatik 20 ölçüm yapılır
   - Dashboard'da istatistikler görünür

2. **Görsel Yükleme:**
   - "Yükle" butonuna tıkla veya sürükle-bırak
   - Ürün seç (dropdown)
   - "Analiz Et" butonuna tıkla

3. **Kamera Kullanımı:**
   - "Kamera" butonuna tıkla
   - Kamera izni ver
   - "Analiz Et" ile anlık görüntü analiz et

---

## 📂 Proje Yapısı

```
demo2/
├── app.html              # Ana uygulama
├── index.html            # Giriş sayfası
├── README.md             # Bu dosya
├── PROJE_RAPORU.md       # Teknik rapor
├── UYGULAMA_DOKUMANI.md  # İşleyiş açıklaması
└── backend/
    ├── color_qc.py       # Backend API
    ├── requirements.txt  # Python bağımlılıkları
    └── venv/             # Virtual environment
```

---

## 🔧 Sorun Giderme

### Backend başlamıyor
```bash
# Port 8001 meşgul mü kontrol et
lsof -ti:8001

# Meşgulse kapat
lsof -ti:8001 | xargs kill -9

# Tekrar başlat
python3 color_qc.py
```

### Frontend açılmıyor
```bash
# Port 3001 meşgul mü kontrol et
lsof -ti:3001

# Meşgulse kapat
lsof -ti:3001 | xargs kill -9

# Tekrar başlat
python3 -m http.server 3001
```

### Modül bulunamıyor hatası
```bash
# Virtual environment aktif mi kontrol et
which python3

# Bağımlılıkları tekrar yükle
pip install -r requirements.txt
```

---

## 📊 API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `http://localhost:8001/analyze/upload` | POST | Görsel yükle ve analiz et |
| `http://localhost:8001/analyze` | POST | Kamera görüntüsünü analiz et |
| `http://localhost:8001/video_feed` | GET | Canlı kamera stream |
| `http://localhost:8001/heatmap_feed` | GET | Renk ısı haritası |
| `http://localhost:8001/dashboard` | GET | İstatistikler |

---

## 🎨 Özellikler

- ✅ Renk analizi (Delta E 2000)
- ✅ Parlaklık ölçümü (0-100 GU)
- ✅ Yüzey pürüzlülüğü tahmini (Ra)
- ✅ Kusur tespiti (çizik, leke, dalga)
- ✅ Renk tutarlılık analizi
- ✅ Kalite sınıflandırma (A+, A, B, C, D)
- ✅ Isı haritası görselleştirme
- ✅ Dashboard ve trend analizi

---

## 📝 Notlar

- Backend çalışmazsa frontend analiz yapamaz
- Kamera kullanımı için HTTPS veya localhost gerekli
- Görsel yükleme için backend'in çalışması şart

---

## 👥 Ekip

**Proje:** OpusAi5  
**Problem:** Problem 2 - Yüzey Parlaklığı ve Eloksal Renk Uyumsuzluğu  
**Kurum:** Aygün Cerrahi Aletler
