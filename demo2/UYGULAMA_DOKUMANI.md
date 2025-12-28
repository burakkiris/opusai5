# OpusAi5 - Uygulama Dokümantasyonu

## Uygulama Ne Yapıyor?

OpusAi5, cerrahi aletlerin **renk kalite kontrolünü** otomatik olarak yapan hibrit yapay zeka tabanlı bir sistemdir.

**Temel İşlev:** Yüklenen ürün görselini analiz ederek:
- Rengin standarda uygun olup olmadığını kontrol eder
- Yüzey parlaklığını ölçer
- Kusurları tespit eder
- Sonuç olarak **ONAY**, **İNCELEME** veya **RED** kararı verir

---

## Nasıl Çalışıyor?

### Adım 1: Görsel Yükleme
Kullanıcı bir ürün görseli yükler veya kamerayı açar.

### Adım 2: Ürün Seçimi
Dropdown'dan analiz edilecek ürün seçilir (örn: Sterilizasyon Konteyneri - RAL 5015)

### Adım 3: Analiz
"Analiz" butonuna tıklanır ve sistem şu işlemleri yapar:

```
Görsel → Renk Analizi → Parlaklık Ölçümü → Kusur Tespiti → Karar
```

### Adım 4: Sonuç
Ekranda analiz sonuçları gösterilir.

---

## Ölçülen Parametreler

### 1. Delta E (Renk Farkı)
**Ne ölçüyor:** Ürün rengi ile standart renk arasındaki fark

**Nasıl çalışıyor:**
1. Görüntünün merkez bölgesinden ortalama renk alınır
2. RGB renk değeri → L*a*b* renk uzayına dönüştürülür
3. Referans renk ile karşılaştırılır
4. CIEDE2000 formülüyle fark hesaplanır

**Sonuç yorumu:**
- ΔE ≤ 1.5 → ✅ UYGUN (Premium kalite)
- ΔE ≤ 2.5 → ⚠️ SINIRDA
- ΔE > 2.5 → ❌ UYGUNSUZ

---

### 2. Parlaklık (Gloss)
**Ne ölçüyor:** Yüzeyin parlaklık seviyesi (0-100 GU)

**Nasıl çalışıyor:**
1. Görüntü gri tonlamaya çevrilir
2. Histogram analizi yapılır
3. Yüksek değerli piksellerin oranı hesaplanır
4. GU (Gloss Unit) değeri üretilir

**Sonuç yorumu:**
- 70+ GU → Yüksek Parlaklık
- 40-70 GU → Orta Parlaklık
- 20-40 GU → Düşük Parlaklık
- <20 GU → Mat

---

### 3. Yüzey Pürüzlülüğü (Ra)
**Ne ölçüyor:** Yüzeyin ne kadar pürüzsüz olduğu (mikron)

**Nasıl çalışıyor:**
1. Laplacian filtresi ile kenar varyansı hesaplanır
2. Sobel gradyanları hesaplanır
3. Bu değerlerden Ra (ortalama pürüzlülük) tahmin edilir

**Sonuç yorumu:**
- Ra < 0.2 μm → Çok Pürüzsüz
- Ra 0.2-0.4 μm → Pürüzsüz
- Ra 0.4-0.8 μm → Normal
- Ra > 0.8 μm → Pürüzlü

---

### 4. Kusur Tespiti
**Ne ölçüyor:** Yüzeydeki çizik, leke ve dalga kusurları

**Nasıl çalışıyor:**
1. Görüntü bulanıklaştırılır (gürültü azaltma)
2. Adaptif eşikleme uygulanır
3. Konturlar bulunur
4. Konturun boyut ve şekline göre kusur tipi belirlenir:
   - Uzun/ince → Çizik
   - Küçük nokta → Leke
   - Geniş alan → Dalga

---

### 5. Renk Tutarlılığı
**Ne ölçüyor:** Yüzey genelinde renk homojenliği

**Nasıl çalışıyor:**
1. Görüntü 3x3 grid'e bölünür (9 bölge)
2. Her bölgenin Delta E değeri hesaplanır
3. Bölgeler arası varyans hesaplanır
4. Tutarlılık yüzdesi üretilir

---

### 6. Kalite Sınıfı
**Ne ölçüyor:** Genel yüzey kalitesi (A+, A, B, C, D)

**Nasıl çalışıyor:**
```
Skor = (Parlaklık × 0.3) + (Pürüzlülük × 0.4) + (Homojenlik × 0.3)

90+ → A+
80-90 → A
70-80 → B
60-70 → C
<60 → D
```

---

### 7. Güven Skoru (Confidence)
**Ne ölçüyor:** Analizin güvenilirlik derecesi

**Nasıl çalışıyor:**
```
Confidence = 95 - (Delta E × 2) - (Kusur sayısı × 2)
```

- Renk farkı düşükse → Yüksek güven
- Kusur azsa → Yüksek güven

---

## Karar Mantığı

```
                    GÖRSEL ANALİZİ
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
      Renk ΔE       Parlaklık        Kusurlar
         │               │               │
         ▼               ▼               ▼
   ΔE ≤ Tolerans?   Aralıkta mı?   Kritik var mı?
         │               │               │
         └───────────────┼───────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
         HEPSİ OK             BİRİ BAŞARISIZ
              │                     │
              ▼                     ▼
           ✅ ONAY              ❌ RED
                            veya ⚠️ İNCELEME
```

---

## Kullanılan Fonksiyonlar

| Fonksiyon | İşlev |
|-----------|-------|
| `rgb_to_lab()` | RGB rengi Lab'a çevirir |
| `calculate_delta_e_2000()` | İki renk arası farkı hesaplar |
| `calculate_gloss()` | Parlaklık değeri hesaplar |
| `detect_surface_defects()` | Kusurları tespit eder |
| `analyze_surface_quality()` | Yüzey kalitesini analiz eder |
| `analyze_color_consistency()` | Renk tutarlılığını ölçer |
| `generate_color_heatmap()` | Renk sapma haritası oluşturur |

---

## Referans Renk Standartları

| Ürün | RAL Kodu | Renk |
|------|----------|------|
| Sterilizasyon Konteyneri | RAL 5015 | 🔵 Mavi |
| Ortopedi Set Kapağı | RAL 6024 | 🟢 Yeşil |
| Forseps Gövdesi | RAL 7042 | ⚫ Gri |
| Acil Set Kapağı | RAL 3020 | 🔴 Kırmızı |
| Nöroşirürji Set | RAL 1023 | 🟡 Sarı |

---

## Örnek Analiz Sonucu

```
Ürün: Sterilizasyon Konteyneri
Durum: ✅ ONAY
Güven: %94.2

Renk Analizi:
  - Ölçülen: L=45.2, a=-8.1, b=-32.3
  - Referans: L=45.5, a=-8.2, b=-32.5
  - Delta E: 0.42 (UYGUN)

Yüzey Kalitesi:
  - Parlaklık: 65.3 GU (Orta)
  - Pürüzlülük: 0.35 Ra (Pürüzsüz)
  - Kalite Sınıfı: A

Kusurlar: 0 adet tespit edildi
```

---

## Kısıtlamalar

⚠️ **Not:** Bu sistem derin öğrenme modeli kullanmamaktadır. Klasik görüntü işleme teknikleri ile çalışır.

**Sınırlamalar:**
- Işık koşullarından etkilenebilir
- Kamera kalibrasyonu gerektirir
- Gerçek spektrofotometre kadar hassas değildir

**İyileştirme önerileri:**
- YOLOv8 ile kusur tespiti
- CNN ile yüzey sınıflandırma
- Spektrofotometre entegrasyonu
