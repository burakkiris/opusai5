# VisionQC - Yapay Zeka Destekli Kalite Kontrol Sistemi

## Problem 1: Ölçüsel Sapmaların Gözden Kaçması - Demo Prototipi

Bu demo, üretim hattında ürünlerin boyutsal ölçümlerini yapan, tolerans kontrolü gerçekleştiren ve otomatik GEÇTİ/KALDI sınıflandırması yapan yapay zeka destekli kalite kontrol sisteminin çalışan prototipdir.

---

## Özellikler

- ✅ Gerçek zamanlı ölçüm simülasyonu
- ✅ 5 farklı cerrahi alet ürün tipi
- ✅ Tolerans bazlı otomatik karar
- ✅ Güven skoru hesaplama
- ✅ Kontrol geçmişi ve istatistikler
- ✅ Modern dashboard arayüzü
- ✅ Otomatik mod (sürekli kontrol)
- ✅ Toplu simülasyon

---

## Hızlı Başlangıç

### 1. Backend Başlatma

```bash
cd demo/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Backend http://localhost:8000 adresinde çalışacak.

### 2. Frontend Başlatma

```bash
cd demo/frontend
npm install
npm start
```

Frontend http://localhost:3000 adresinde açılacak.

---

## Ürün Kataloğu

| Kod | Ürün | Uzunluk | Genişlik | Yükseklik |
|-----|------|---------|----------|-----------|
| FRC-180-STD | Doku Forsepsi Standart | 180mm ±1.0 | 12mm ±0.3 | 8mm ±0.2 |
| SCR-120-PRO | Cerrahi Makas Pro | 120mm ±0.8 | 15mm ±0.4 | 6mm ±0.3 |
| CLM-090-ECO | Klemp Ekonomik | 90mm ±0.5 | 8mm ±0.2 | 5mm ±0.15 |
| RTR-150-MED | Retraktör Medikal | 150mm ±1.2 | 20mm ±0.5 | 10mm ±0.4 |
| NHD-080-PRE | İğne Tutucu Presizyon | 80mm ±0.3 | 6mm ±0.15 | 4mm ±0.1 |

---

## API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | /products | Tüm ürünleri listele |
| GET | /products/{code} | Ürün detayı |
| POST | /simulate?product_code=XXX | Tek kontrol simülasyonu |
| POST | /batch-simulate?count=N | Toplu simülasyon |
| GET | /dashboard | Dashboard istatistikleri |
| GET | /history | Kontrol geçmişi |

---

## Teknolojiler

**Backend:**
- Python 3.10+
- FastAPI
- OpenCV
- NumPy

**Frontend:**
- React 18
- TailwindCSS
- Axios
- Lucide Icons

---

## Yarışma Bilgisi

**Yarışma:** Yapay Zeka ile Yerel Dönüşüm Atölyesi 2025  
**Problem:** Problem 1 - Ölçüsel Sapmaların Gözden Kaçması  
**Çözüm:** VisionQC - Machine Vision ile Otomatik Kalite Kontrol

---

*Bu demo, konsept kanıtlama (Proof of Concept) amaçlıdır.*
