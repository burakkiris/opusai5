# YAPAY ZEKÂ İLE YEREL DÖNÜŞÜM ATÖLYESİ
## Öğrenci Çözüm Raporu

---

# KAPAK

**Takım Adı:** [Takım Adınız]

**Takım Üyeleri:**
1. [İsim 1] - [Bölüm]
2. [İsim 2] - [Bölüm]
3. [İsim 3] - [Bölüm]
4. [İsim 4] - [Bölüm]

**Seçilen Problem:** Problem 1 – Ölçüsel Sapmaların Gözden Kaçması

**Çözüm Adı:** VisionQC – Yapay Zekâ Destekli Akıllı Ölçüsel Kalite Kontrol Sistemi

**Tarih:** 27-28 Aralık 2025

---

# 1. PROBLEM ANALİZİ

## 1.1 Mevcut Durum

Üretim sektöründe kalite kontrol süreçleri büyük ölçüde **insan gözüne ve manuel ölçüm araçlarına** bağlıdır. Özellikle hassas parça üreten sektörlerde (medikal cihazlar, havacılık, otomotiv, savunma sanayi) ölçüsel sapmalar kritik önem taşır.

**Manuel Kalite Kontrol Süreci:**
```
Ürün Üretimi → Manuel Ölçüm (Kumpas/Mikrometre) → Görsel İnceleme → Onay/Red Kararı
```

**Mevcut Sistemin Zayıflıkları:**

| Sorun | Açıklama |
|-------|----------|
| **İnsan Hatası** | Yorgunluk, dikkat dağınıklığı, öznel değerlendirme |
| **Tutarsızlık** | Farklı operatörler farklı sonuçlar üretebilir |
| **Yavaşlık** | Her ürün için 30-60 saniye arası kontrol süresi |
| **Kayıt Eksikliği** | Dijital veri kaydı yetersiz, trend analizi yapılamıyor |
| **Örneklem Sınırlılığı** | Tüm ürünler kontrol edilemiyor, %10-20 örneklem |

## 1.2 Problemin Üretime Etkisi

### Doğrudan Etkiler:

1. **Hatalı Ürün Müşteriye Ulaşması**
   - Müşteri şikayetleri ve iade maliyetleri
   - Marka itibarının zedelenmesi
   - Uzun vadeli müşteri kaybı

2. **Ekonomik Kayıplar**
   - Reddedilen ürünlerde hammadde israfı
   - Yeniden işleme (rework) maliyetleri
   - Garanti kapsamında ücretsiz değişim/tamir

3. **Operasyonel Sorunlar**
   - Darboğaz oluşumu (kalite kontrol noktasında birikim)
   - Teslimat gecikmesi
   - Planlama belirsizliği

### Sektörel Örnekler:

**Medikal Cihaz Sektörü (Cerrahi Alet Üretimi):**
Cerrahi aletlerde tolerans değerleri son derece sıkıdır. Örneğin, bir forseps'in kavrama yüzeylerindeki 0.2mm'lik sapma, ameliyat sırasında doku tutma performansını doğrudan etkiler. Aygün Cerrahi Aletler gibi medikal cihaz üreticilerinde bu durum hasta güvenliği ile doğrudan ilişkilidir ve FDA/CE regülasyonlarına uyum zorunluluğu vardır.

**Otomotiv Sektörü:**
Motor parçalarındaki ölçüsel sapmalar, performans kaybı ve erken arızaya neden olur.

**Havacılık Sektörü:**
Uçak parçalarındaki mikron düzeyinde sapmalar bile güvenlik riski oluşturur.

## 1.3 Neden Kritik?

### İş Sürekliliği Açısından:
- **%100 kontrol imkânsızlığı:** Manuel yöntemle her ürünü kontrol etmek maliyet-etkin değil
- **Reaktif yaklaşım:** Hatalar müşteriden geri dönüşle anlaşılıyor
- **Veri eksikliği:** Süreç iyileştirme için gerekli analitik altyapı yok

### Rekabet Açısından:
- Rakipler otomasyon ve yapay zekâ yatırımları yapıyor
- Müşteri beklentileri artıyor (sıfır hata toleransı)
- Maliyet baskısı yoğunlaşıyor

### Regülasyon Açısından:
- ISO 9001 kalite yönetim sistemi gereksinimleri
- Sektörel standartlar (ISO 13485 - Medikal Cihazlar)
- İzlenebilirlik ve dokümantasyon zorunlulukları

---

# 2. ÇÖZÜM ÖNERİSİ

## 2.1 VisionQC - Genel Bakış

**VisionQC**, üretim hattında gerçek zamanlı olarak ürünlerin boyutsal ölçümlerini yapan, tolerans kontrolü gerçekleştiren ve otomatik geçti/kaldı sınıflandırması yapan **yapay zekâ destekli görüntü işleme sistemidir**.

### Temel Özellikler:
- ✅ %100 ürün kontrolü (örneklem değil, tüm ürünler)
- ✅ 2-3 saniye/ürün kontrol hızı
- ✅ %99+ doğruluk oranı
- ✅ Otomatik veri kaydı ve trend analizi
- ✅ Gerçek zamanlı uyarı sistemi
- ✅ Entegre raporlama dashboard'u

## 2.2 Kullanılan Teknolojiler

| Kategori | Teknoloji | Kullanım Amacı |
|----------|-----------|----------------|
| **Görüntü İşleme** | OpenCV | Kenar tespiti, kontur analizi, ölçüm |
| **Makine Öğrenmesi** | TensorFlow/PyTorch | Anomali tespiti, kalite sınıflandırma |
| **Nesne Tespiti** | YOLOv8 | Ürün lokalizasyonu ve segmentasyonu |
| **Backend** | Python + FastAPI | API servisleri, iş mantığı |
| **Frontend** | React + TailwindCSS | Operatör arayüzü, dashboard |
| **Veritabanı** | PostgreSQL + InfluxDB | Kayıt ve zaman serisi verileri |
| **Görselleştirme** | Grafana / Chart.js | Analitik dashboard |

## 2.3 Modelin Temel Mantığı

### Aşama 1: Görüntü Yakalama
```
┌─────────────────────────────────────────────────────────┐
│  ENDÜSTRİYEL KAMERA SİSTEMİ                            │
│  ─────────────────────────────                          │
│  • Sabit pozisyonlu kamera (üstten/yandan görünüm)     │
│  • Kontrollü LED aydınlatma (gölge/yansıma eliminasyonu)│
│  • Tetikleme: Sensör veya PLC sinyali                  │
│  • Çözünürlük: 2-5 MP (hassasiyete göre)               │
└─────────────────────────────────────────────────────────┘
```

### Aşama 2: Görüntü Ön İşleme
```python
# Pseudo-kod
1. Gürültü azaltma (Gaussian Blur)
2. Kontrast iyileştirme (CLAHE)
3. Renk uzayı dönüşümü (BGR → Grayscale)
4. Adaptif eşikleme (Thresholding)
5. Morfolojik operasyonlar (Erosion/Dilation)
```

### Aşama 3: Ölçüm Algoritması
```
┌─────────────────────────────────────────────────────────┐
│  ÖLÇÜM MOTORU                                          │
│  ─────────────                                          │
│  1. Kenar Tespiti (Canny Edge Detection)               │
│  2. Kontur Çıkarımı (findContours)                     │
│  3. Minimum Çevreleyen Dikdörtgen (minAreaRect)        │
│  4. Piksel → Milimetre Dönüşümü (Kalibrasyon faktörü)  │
│  5. En x Boy x Yükseklik hesaplama                     │
└─────────────────────────────────────────────────────────┘
```

**Kalibrasyon:** Bilinen boyutlardaki referans obje ile piksel/mm oranı hesaplanır.

### Aşama 4: Tolerans Karşılaştırma ve Sınıflandırma
```
┌─────────────────────────────────────────────────────────┐
│  KARAR MOTORU                                          │
│  ───────────                                            │
│                                                         │
│  Ölçülen Değer: 25.3 mm                                │
│  Nominal Değer: 25.0 mm                                │
│  Tolerans: ±0.5 mm                                     │
│  Alt Limit: 24.5 mm | Üst Limit: 25.5 mm              │
│                                                         │
│  Sapma: +0.3 mm                                        │
│  Sonuç: ✅ GEÇTİ (tolerans içinde)                     │
│  Güven Skoru: %97.8                                    │
└─────────────────────────────────────────────────────────┘
```

### Aşama 5: ML ile Gelişmiş Anomali Tespiti
Temel ölçüm algoritmasına ek olarak, **makine öğrenmesi modeli** şu durumları tespit eder:
- Çizik, çatlak gibi yüzey kusurları
- Geometrik deformasyonlar
- Beklenmedik şekil sapmaları

## 2.4 Veri Giriş-Çıkış Yapısı

### GİRİŞLER:

| Veri | Kaynak | Format |
|------|--------|--------|
| Ürün görüntüsü | Endüstriyel kamera | JPEG/PNG (2048x1536) |
| Ürün kodu | Barkod/QR okuyucu veya manuel | String |
| Ürün spesifikasyonları | Veritabanı | JSON (nominal değerler + toleranslar) |
| Kalibrasyon parametreleri | Sistem ayarları | Float (px/mm) |

### ÇIKIŞLAR:

| Veri | Açıklama | Format |
|------|----------|--------|
| Boyut ölçümleri | En, boy, yükseklik (mm) | Float array |
| Sapma değerleri | Nominal değerden fark | Float array |
| Karar | GEÇTİ / KALDI | Boolean + String |
| Güven skoru | Model kesinlik derecesi | Float (0-100%) |
| İşaretli görüntü | Ölçüm noktaları gösterimli | PNG |
| Hata detayı | Hangi ölçü neden kaldı | String |
| Zaman damgası | Kontrol zamanı | ISO 8601 |

## 2.5 Sistem Akış Diyagramı

```
                              VisionQC SİSTEM AKIŞI
    ═══════════════════════════════════════════════════════════════════

    ┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────┐
    │  ÜRETİM  │────▶│  SENSÖR  │────▶│    KAMERA    │────▶│  GÖRÜNTÜ │
    │  HATTI   │     │ TETİKLER │     │   YAKALAR    │     │  SUNUCU  │
    └──────────┘     └──────────┘     └──────────────┘     └────┬─────┘
                                                                 │
         ┌───────────────────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                      GÖRÜNTÜ İŞLEME PIPELINE                     │
    │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐  │
    │  │ Ön İşleme│──▶│  Kenar   │──▶│  Kontur  │──▶│   Boyut      │  │
    │  │ (Filtre) │   │  Tespiti │   │  Analizi │   │   Hesaplama  │  │
    │  └──────────┘   └──────────┘   └──────────┘   └──────────────┘  │
    └──────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                       KARAR MOTORU                               │
    │                                                                  │
    │   Ölçülen Değerler    Ürün Spesifikasyonu    Tolerans Kontrolü  │
    │   ───────────────  +  ─────────────────── →  ─────────────────  │
    │   [25.3, 10.1, 5.2]   [25.0, 10.0, 5.0]      [±0.5, ±0.3, ±0.2] │
    │                                                                  │
    │                           │                                      │
    │                           ▼                                      │
    │                  ┌─────────────────┐                            │
    │                  │  SINIFLANDIRMA  │                            │
    │                  │  ✅ GEÇTİ       │                            │
    │                  │  ❌ KALDI       │                            │
    │                  └─────────────────┘                            │
    └──────────────────────────────────────────────────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
             ┌────────────┐      ┌─────────────┐      ┌─────────────┐
             │  VERİTABANI │      │  OPERATÖR   │      │   FIZIKSEL  │
             │   KAYIT     │      │  DASHBOARD  │      │   AYIRMA    │
             │             │      │  (Anlık)    │      │  (Reject)   │
             └────────────┘      └─────────────┘      └─────────────┘
                    │
                    ▼
             ┌─────────────────────────────────────────────┐
             │            ANALİTİK KATMAN                  │
             │  • Trend Grafikleri                         │
             │  • Vardiya Bazlı Performans                 │
             │  • Makine/Operatör Korelasyonu             │
             │  • Tahminsel Kalite (Predictive QC)        │
             └─────────────────────────────────────────────┘
```

## 2.6 Örnek Uygulama: Cerrahi Alet Üretimi

**Senaryo:** Aygün Cerrahi Aletler üretim hattında forseps kalite kontrolü

### Ürün: Doku Forsepsi
- **Nominal Boyutlar:** Uzunluk: 180mm, Genişlik: 12mm, Kavrama Açısı: 45°
- **Kritik Toleranslar:** 
  - Uzunluk: ±1.0mm
  - Genişlik: ±0.3mm
  - Kavrama açısı: ±2°

### VisionQC Kontrol Çıktısı:
```
╔══════════════════════════════════════════════════════════════╗
║  VisionQC - Ölçüm Raporu                                    ║
╠══════════════════════════════════════════════════════════════╣
║  Ürün Kodu    : FRC-180-STD                                 ║
║  Parti No     : 2025-12-27-045                              ║
║  Kontrol Zamanı: 14:32:15                                   ║
╠══════════════════════════════════════════════════════════════╣
║  ÖLÇÜM SONUÇLARI                                            ║
║  ──────────────                                              ║
║  Parametre      Ölçülen    Nominal    Sapma     Durum       ║
║  ─────────────────────────────────────────────────────       ║
║  Uzunluk        179.8 mm   180.0 mm   -0.2 mm   ✅ GEÇTİ    ║
║  Genişlik        12.1 mm    12.0 mm   +0.1 mm   ✅ GEÇTİ    ║
║  Kavrama Açısı   44.5°      45.0°     -0.5°    ✅ GEÇTİ    ║
╠══════════════════════════════════════════════════════════════╣
║  GENEL SONUÇ: ✅ GEÇTİ                                       ║
║  Güven Skoru : %98.5                                        ║
║  Kontrol Süresi: 2.3 saniye                                 ║
╚══════════════════════════════════════════════════════════════╝
```

---

# 3. KATKI VE ETKİ ANALİZİ

## 3.1 Kalite Artışı

| Metrik | Mevcut (Manuel) | VisionQC Sonrası | İyileşme |
|--------|-----------------|------------------|----------|
| Tespit doğruluğu | %85-90 | %99+ | **+10-14%** |
| Kontrol kapsamı | %15-20 (örneklem) | %100 | **+80-85%** |
| Tutarlılık | Operatöre bağlı değişken | Sabit, tekrarlanabilir | **Standartlaşma** |
| Müşteri iade oranı | %2-3 | <%0.5 | **%80+ azalma** |

### Kalite İyileştirme Döngüsü:
```
     ┌────────────────────────────────────────────────────┐
     │                                                    │
     ▼                                                    │
 ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐   │
 │ Ölçüm  │───▶│  Veri  │───▶│ Analiz │───▶│ Önlem  │───┘
 │        │    │ Kayıt  │    │        │    │        │
 └────────┘    └────────┘    └────────┘    └────────┘
     │
     └──▶ Her üründen veri → Sürekli iyileştirme döngüsü
```

## 3.2 Maliyet Düşüşü

### Yıllık Maliyet Analizi (Örnek Senaryo)

**Varsayımlar:**
- Yıllık üretim: 100.000 adet
- Birim üretim maliyeti: 50 TL
- Mevcut hata oranı: %3 (3.000 adet/yıl)
- Hatalı ürün başına kayıp: 75 TL (malzeme + işçilik + fırsat maliyeti)

| Kalem | Mevcut Maliyet | VisionQC Sonrası | Tasarruf |
|-------|----------------|------------------|----------|
| Hatalı ürün kaybı | 225.000 TL | 37.500 TL | **187.500 TL** |
| Müşteri iade maliyeti | 50.000 TL | 5.000 TL | **45.000 TL** |
| Yeniden işleme | 30.000 TL | 5.000 TL | **25.000 TL** |
| Kalite kontrol personeli | 180.000 TL | 60.000 TL | **120.000 TL** |
| **TOPLAM YILLIK TASARRUF** | | | **377.500 TL** |

**ROI Hesabı:**
- Sistem yatırım maliyeti (tahmini): 150.000 TL
- Geri ödeme süresi: **~5 ay**

## 3.3 Zaman Tasarrufu

| Süreç | Mevcut | VisionQC | Kazanç |
|-------|--------|----------|--------|
| Ürün başına kontrol | 45 saniye | 3 saniye | **%93** |
| Vardiya başına kontrol kapasitesi | 400 adet | 6.000 adet | **15x** |
| Raporlama | 2 saat/gün (manuel) | Otomatik, anlık | **2 saat/gün** |
| Hata analizi | 1-2 gün | Anlık | **%99** |

### Darboğaz Eliminasyonu:
Manuel kontrol noktası genellikle üretim hattının en yavaş noktasıdır. VisionQC ile bu darboğaz ortadan kalkar.

## 3.4 Sürdürülebilirlik Katkısı

### Çevresel Etki:

| Alan | Katkı |
|------|-------|
| **Hammadde Tasarrufu** | Daha az fire = daha az metal/plastik tüketimi |
| **Enerji Verimliliği** | Yeniden işleme azalması = enerji tasarrufu |
| **Karbon Ayak İzi** | İade/değişim lojistiğinin azalması |
| **Dijitalleşme** | Kağıt bazlı kayıtların eliminasyonu |

### ISO 14001 ve Yeşil Üretim Uyumu:
- Kaynak verimliliği metrikleri otomatik takip
- Çevresel performans raporlaması
- Sürdürülebilirlik hedeflerine katkı

---

# 4. PROTOTİP / MOCKUP

## 4.1 Operatör Dashboard Tasarımı

```
┌──────────────────────────────────────────────────────────────────────────┐
│  VisionQC Dashboard                                    👤 Operatör: Ali  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐│
│  │     SON KONTROL                 │  │     GÜNLÜK ÖZET                ││
│  │  ┌───────────────────────────┐  │  │                                ││
│  │  │                           │  │  │  Toplam Kontrol: 1.247         ││
│  │  │      [ÜRÜN GÖRÜNTÜSÜ]     │  │  │  ✅ Geçti: 1.198 (%96.1)       ││
│  │  │                           │  │  │  ❌ Kaldı: 49 (%3.9)           ││
│  │  │   ← 180.2mm →             │  │  │                                ││
│  │  │   ↕ 12.1mm                │  │  │  ┌────────────────────────┐    ││
│  │  └───────────────────────────┘  │  │  │ ████████████░░ %96.1   │    ││
│  │                                 │  │  └────────────────────────┘    ││
│  │  ✅ GEÇTİ - Güven: %98.5        │  │                                ││
│  │  Süre: 2.3s                     │  │  Ortalama Süre: 2.8s           ││
│  └─────────────────────────────────┘  └─────────────────────────────────┘│
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────────┤
│  │  SON 50 KONTROL TRENDİ                                               │
│  │  ──────────────────────────────────────────────────────────────────  │
│  │       ✅✅✅✅✅❌✅✅✅✅✅✅✅✅✅✅✅✅❌✅✅✅✅✅✅               │
│  │       ✅✅✅✅✅✅✅✅✅✅✅✅❌✅✅✅✅✅✅✅✅✅✅✅✅               │
│  │                                                                      │
│  │  [!] Uyarı: Son 1 saatte red oranı %4.2 - normalin üzerinde         │
│  └──────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────────┤
│  │  SAPMA TRENDİ (Uzunluk - Son 100 ürün)                               │
│  │                                                                      │
│  │  +0.5 ┤                    ╭─╮                                       │
│  │  +0.3 ┤     ╭──╮     ╭────╯ ╰──╮                                    │
│  │   0.0 ┼────╯  ╰─────╯          ╰────────────────── Nominal          │
│  │  -0.3 ┤                                     ╭──╮                     │
│  │  -0.5 ┤                                    ╯  ╰─                     │
│  │       └──────────────────────────────────────────▶                   │
│  └──────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Yönetici Raporlama Ekranı

```
┌──────────────────────────────────────────────────────────────────────────┐
│  VisionQC - Yönetici Paneli                           📅 Aralık 2025    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────┐│
│  │   TOPLAM       │ │   GEÇTİ        │ │   KALDI        │ │   ORT SÜRE ││
│  │   32.456       │ │   31.203       │ │   1.253        │ │   2.4s     ││
│  │   adet/ay      │ │   %96.1        │ │   %3.9         │ │   /ürün    ││
│  └────────────────┘ └────────────────┘ └────────────────┘ └────────────┘│
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  ÜRÜN BAZLI RED DAĞILIMI                                          │ │
│  │  ──────────────────────                                            │ │
│  │  FRC-180-STD  ████████████████░░░░ 320 adet (%25.5)               │ │
│  │  SCR-120-PRO  ██████████░░░░░░░░░░ 198 adet (%15.8)               │ │
│  │  CLM-090-ECO  ████████░░░░░░░░░░░░ 156 adet (%12.4)               │ │
│  │  Diğer        ██████████████████░░ 579 adet (%46.3)               │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  RED NEDENLERİ                                                     │ │
│  │  ─────────────                                                     │ │
│  │  • Uzunluk tolerans aşımı: 42%                                    │ │
│  │  • Genişlik tolerans aşımı: 28%                                   │ │
│  │  • Açı sapması: 18%                                               │ │
│  │  • Yüzey kusuru: 12%                                              │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  [📊 Detaylı Rapor İndir]  [📧 Raporu E-posta Gönder]  [🖨️ Yazdır]      │
└──────────────────────────────────────────────────────────────────────────┘
```

## 4.3 Uyarı/Alarm Ekranı

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ⚠️  ALARM - VisionQC                                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ╔════════════════════════════════════════════════════════════════════╗ │
│  ║  🔴 KRİTİK: Ardışık 5 ürün RED aldı!                              ║ │
│  ║                                                                    ║ │
│  ║  Hat: Üretim Hattı 3                                              ║ │
│  ║  Ürün: FRC-180-STD                                                ║ │
│  ║  Zaman: 14:45:23                                                   ║ │
│  ║                                                                    ║ │
│  ║  Son 5 Ürün Red Nedeni:                                           ║ │
│  ║  • Uzunluk: 181.2mm (Limit: 181.0mm) - Sapma: +1.2mm             ║ │
│  ║  • Uzunluk: 181.4mm (Limit: 181.0mm) - Sapma: +1.4mm             ║ │
│  ║  • Uzunluk: 181.3mm (Limit: 181.0mm) - Sapma: +1.3mm             ║ │
│  ║  • Uzunluk: 181.5mm (Limit: 181.0mm) - Sapma: +1.5mm             ║ │
│  ║  • Uzunluk: 181.2mm (Limit: 181.0mm) - Sapma: +1.2mm             ║ │
│  ║                                                                    ║ │
│  ║  ÖNERİ: CNC makinesinde takım aşınması olabilir. Kontrol edin.   ║ │
│  ║                                                                    ║ │
│  ║  [Onayla ve Kapat]  [Bakım Ekibine Bildir]  [Hattı Durdur]       ║ │
│  ╚════════════════════════════════════════════════════════════════════╝ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

# 5. UYGULANABİLİRLİK VE YOL HARİTASI

## 5.1 Uygulama Fazları

### Faz 1: Pilot Uygulama (0-3 Ay)

| Hafta | Aktivite |
|-------|----------|
| 1-2 | İhtiyaç analizi, donanım seçimi, ortam hazırlığı |
| 3-4 | Kamera ve aydınlatma kurulumu, kalibrasyon |
| 5-8 | Yazılım geliştirme, ürün bazlı model eğitimi |
| 9-10 | Test ve validasyon (paralel çalışma: manuel + otomatik) |
| 11-12 | Operatör eğitimi, fine-tuning, devreye alma |

**Pilot Kapsam:** 1 üretim hattı, 3-5 ürün tipi

### Faz 2: Yaygınlaştırma (3-6 Ay)

| Aktivite | Detay |
|----------|-------|
| Diğer hatlara genişleme | Pilot başarısına göre 2-3 hat daha |
| Ürün kataloğu genişletme | 20-30 ürün tipine çıkış |
| ERP entegrasyonu | SAP/Logo vb. sistemlerle veri paylaşımı |
| Raporlama otomasyonu | Otomatik günlük/haftalık raporlar |

### Faz 3: Optimizasyon (6-12 Ay)

| Aktivite | Detay |
|----------|-------|
| Tahminsel kalite | ML ile hata öncesi uyarı sistemi |
| Makine korelasyonu | Hangi makine hangi hatayı üretiyor analizi |
| Tedarikçi kalite takibi | Hammadde bazlı kalite skorlaması |
| Sürekli öğrenme | Model performansının otomatik iyileştirilmesi |

## 5.2 Pilot Uygulama Önerisi

**Hedef:** Cerrahi alet üretim hattında forseps kalite kontrolü

**Neden Bu Ürün?**
- Yüksek üretim adedi (yeterli veri)
- Kritik toleranslar (yüksek etki)
- Standart geometri (kolay başlangıç)

**Başarı Kriterleri:**
- ✅ %99 tespit doğruluğu
- ✅ <3 saniye kontrol süresi
- ✅ %0 yanlış pozitif (iyi ürünü reddetme)
- ✅ Operatör memnuniyeti

## 5.3 Risk Analizi ve Azaltma

| Risk | Olasılık | Etki | Azaltma Stratejisi |
|------|----------|------|---------------------|
| Işık/ortam değişkenliği | Orta | Yüksek | Kontrollü aydınlatma kabini |
| Yansımalı yüzeyler | Yüksek | Orta | Polarize ışık, çoklu açı |
| Model doğruluğu | Düşük | Yüksek | Kapsamlı test, paralel çalışma dönemi |
| Operatör direnci | Orta | Orta | Eğitim, kullanım kolaylığı, fayda gösterimi |
| Sistem arızası | Düşük | Yüksek | Yedeklilik, manuel mod, SLA |

---

# 6. SONUÇ

## Özet

VisionQC, üretim sektöründe kritik bir soruna – **ölçüsel sapmaların gözden kaçması** – yapay zekâ ve görüntü işleme teknolojileri ile **uygulanabilir, ölçeklenebilir ve sürdürülebilir** bir çözüm sunmaktadır.

## Temel Faydalar

| Fayda | Etki |
|-------|------|
| **%100 Kontrol** | Örneklem yerine tüm ürünler |
| **%99+ Doğruluk** | İnsan hatasını elimine etme |
| **15x Hız Artışı** | 45 saniye → 3 saniye |
| **%80+ Maliyet Düşüşü** | Fire ve iade azalması |
| **Veri Odaklı İyileştirme** | Sürekli öğrenme döngüsü |

## Firmaya Katma Değer

Cerrahi alet üreticileri başta olmak üzere hassas parça üreten tüm firmalar için VisionQC:

1. **Kalite standardını yükseltir** → Müşteri memnuniyeti ve sadakati
2. **Maliyetleri düşürür** → Rekabet avantajı
3. **Regülasyona uyumu kolaylaştırır** → İzlenebilirlik ve dokümantasyon
4. **Sürdürülebilirliğe katkı sağlar** → Kaynak verimliliği

## Kapanış

> "Ölçemediğinizi yönetemezsiniz." - Peter Drucker

VisionQC ile sadece ölçmekle kalmıyor, **akıllıca analiz ediyor ve sürekli iyileştiriyoruz**.

---

# EKLER

## Ek A: Teknik Gereksinimler

### Donanım:
- Endüstriyel kamera (2-5 MP, GigE veya USB3)
- LED ring/bar aydınlatma
- Bilgisayar (i7/Ryzen 7, 16GB RAM, GPU opsiyonel)
- Montaj ekipmanları

### Yazılım:
- Python 3.10+
- OpenCV 4.x
- TensorFlow 2.x / PyTorch 2.x
- FastAPI
- React 18+
- PostgreSQL 15+

## Ek B: Referans Akademik Çalışmalar

1. "Deep Learning for Industrial Quality Control" - IEEE 2023
2. "Computer Vision in Manufacturing" - Springer 2024
3. "Automated Dimensional Measurement Systems" - CIRP 2022

## Ek C: Örnek Kod Snippet

```python
import cv2
import numpy as np

def measure_dimensions(image_path, pixels_per_mm):
    """Ürün boyutlarını ölç ve döndür"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Kenar tespiti
    edges = cv2.Canny(gray, 50, 150)
    
    # Kontur bulma
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(largest)
        width_px, height_px = rect[1]
        
        # Piksel → mm dönüşümü
        width_mm = width_px / pixels_per_mm
        height_mm = height_px / pixels_per_mm
        
        return {"width_mm": width_mm, "height_mm": height_mm}
    
    return None
```

---

**Rapor Sonu**

*Bu rapor, Yapay Zekâ ile Yerel Dönüşüm Atölyesi kapsamında hazırlanmıştır.*
