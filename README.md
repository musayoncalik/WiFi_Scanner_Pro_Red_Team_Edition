# 🔍 WiFi Scanner Pro - Pasif WiFi Analiz ve Güvenlik Değerlendirme Aracı

**Bitirme Projesi**  
**Öğrenci:** Musa Yoncalık  
**Proje Türü:** Güvenlik ve Ağ Analizi  
**Dil:** Python 3.11+  # 🔍 WiFi Scanner Pro - Pasif WiFi Analiz ve Güvenlik Değerlendirme Aracı

**Bitirme Projesi**  
**Öğrenci:** Musa Yoncalık  
**Proje Türü:** Güvenlik ve Ağ Analizi  
**Dil:** Python 3.11+  
**Platform:** Kali Linux  
**Versiyon:** 2.0  
**Durum:** ✅ Tamamlandı - Production Ready

---

## 📋 İçindekiler

1. [Proje Özeti](#proje-özeti)
2. [Proje Amacı](#proje-amacı)
3. [Özellikler](#özellikler)
4. [Teknolojiler](#teknolojiler)
5. [Kurulum](#kurulum)
6. [Kullanım](#kullanım)
7. [Proje Yapısı](#proje-yapısı)
8. [Modüller ve Bileşenler](#modüller-ve-bileşenler)
9. [Test](#test)
10. [Ekran Görüntüleri](#ekran-görüntüleri)
11. [Etik Kullanım ve Yasal Uyarı](#etik-kullanım-ve-yasal-uyarı)
12. [Gelecek Geliştirmeler](#gelecek-geliştirmeler)
13. [Kaynaklar](#kaynaklar)

---

## 🎯 Proje Özeti

**WiFi Scanner Pro**, Kali Linux üzerinde çalışan, tamamen **pasif analiz prensibine dayalı**, ultra modern ve profesyonel bir masaüstü uygulamasıdır. Proje, çevredeki Wi-Fi ağlarını gerçek zamanlı olarak analiz etmek, detaylı güvenlik değerlendirmesi yapmak ve kullanıcıda ağ güvenliği konusunda farkındalık oluşturmak amacıyla geliştirilmiştir.

### ✨ Temel Özellikler

- ✅ **Tamamen Pasif Analiz**: Hiçbir paket gönderilmez, sadece dinleme yapılır
- ✅ **Gerçek Zamanlı İzleme**: Canlı grafikler ve anlık güncellemeler
- ✅ **Gelişmiş IDS**: Saldırı tespiti ve güvenlik analizi
- ✅ **Profesyonel Raporlama**: PDF, HTML ve CSV formatlarında raporlar
- ✅ **Ultra Modern GUI**: Gradient renkler, ikonlar, glassmorphism efektleri
- ✅ **Detaylı Güvenlik Analizi**: WPA2-PSK (CCMP), WPA3-SAE, WPS, PMF tespiti
- ✅ **Vendor Tespiti**: manuf kütüphanesi ile gerçek üretici bilgisi
- ✅ **Client-AP İlişkisi**: Data frame analizi ile bağlı cihaz tespiti
- ✅ **Risk Skoru Hesaplama**: Yüzdesel risk değerlendirmesi
- ✅ **Detay Paneli**: Sağdan açılan, sekmeli detay görüntüleme

---

## 🎓 Proje Amacı

Bu proje, özellikle teknik bilgisi sınırlı kullanıcıların dahi Wi-Fi ortamlarını anlayabilmesini ve olası riskleri fark edebilmesini hedefler. 
Kısaca ; Wifi ağına bağlanmadan, pasif olarak ortamı dinleyerek kablosuz ağların ve cihazların güvenlik durumunu analiz eden bir araçtır. 

Uygulama:

- Kablosuz ağlardan yayılan paketleri **pasif olarak** dinleyerek analiz eder
- Ağ adı (SSID), MAC adresi (BSSID), sinyal gücü (RSSI), kanal bilgisi ve **detaylı güvenlik protokollerini** tespit eder
- Bu verileri güvenlik, performans ve IDS modülleri ile analiz eder
- Elde edilen sonuçları **modern grafikler** ve detaylı raporlar halinde kullanıcıya sunar
- **Saldırı veya ağa müdahale içermeyen** yapısıyla etik ve yasal sınırlar içinde kalır

---

## ✨ Özellikler

### 🔍 Temel Analiz Özellikleri

#### Pasif WiFi Tarama
- Monitor mode'da paket yakalama (Scapy)
- Otomatik kanal atlama (2.4GHz ve 5GHz)
- Beacon, Probe Request ve **Data frame** analizi
- Gerçek zamanlı ağ keşfi
- Multi-threaded paket işleme

#### Ağ Bilgisi Çıkarımı
- **SSID**: Ağ adı tespiti (Hidden ağ desteği)
- **BSSID**: MAC adresi
- **Kanal**: 2.4GHz ve 5GHz kanal bilgisi
- **RSSI**: Sinyal gücü ölçümü (dBm)
- **Güvenlik Protokolü**: Detaylı tespit (WPA2-PSK (CCMP), WPA3-SAE, WEP, Open)
- **Vendor Bilgisi**: manuf kütüphanesi ile gerçek üretici tespiti (Apple, Samsung, TP-Link, vb.)
- **Risk Skoru**: Yüzdesel risk değerlendirmesi (0-100%)

#### Detaylı Güvenlik Analizi
- **WPA2-PSK (CCMP)**: Güçlü şifreleme tespiti
- **WPA2-PSK (TKIP)**: Zayıf şifreleme uyarısı
- **WPA3-SAE**: En güvenli protokol
- **WPS Durumu**: WPS açık/kapalı tespiti
- **PMF (Protected Management Frames)**: PMF zorunlu/destekli tespiti
- **WEP**: Güvensiz protokol uyarısı
- **Open Network**: Şifreleme yok uyarısı

#### Client-AP İlişkisi Tespiti
- **Data Frame Analizi**: Hangi cihazın hangi AP'ye bağlı olduğunu tespit
- **Client MAC**: Bağlı cihaz MAC adresleri
- **Vendor Tespiti**: Client cihaz üretici bilgisi
- **Device Type**: Telefon, Laptop, Router tespiti
- **Frame Count**: Trafik analizi
- **RSSI Tracking**: Client sinyal gücü takibi

#### SNR ve Performans Analizi
- **SNR Hesaplama**: Signal-to-Noise Ratio analizi
- **Noise Floor**: Gürültü seviyesi tespiti
- **Kanal Overlap Matrisi**: Kanal girişim analizi
- **DFS Desteği**: 5GHz radar bantları tespiti
- **En İyi Kanal Önerisi**: Otomatik kanal optimizasyonu

### 🛡️ Güvenlik Özellikleri

#### IDS (Intrusion Detection System)
- **Deauth Flood Tespiti**: Deauthentication saldırıları
- **Probe Storm Tespiti**: Probe request fırtınaları
- **Beacon Flood Tespiti**: Beacon frame saldırıları
- **Association Flood Tespiti**: Association request saldırıları
- **MAC Spoofing Tespiti**: Şüpheli MAC adresi aktiviteleri
- **Gerçek Zamanlı Uyarılar**: Anlık saldırı bildirimleri

#### Rogue AP Tespiti
- **Evil Twin Tespiti**: Aynı SSID'ye sahip sahte erişim noktaları
- **Vendor Uyumsuzluğu**: Farklı üreticilerden aynı SSID
- **Güvenlik Protokolü Farklılığı**: Open vs şifreli ağ tespiti
- **Kanal Yakınlığı**: Şüpheli kanal dağılımı
- **Risk Skoru Hesaplama**: Yüzdesel risk değerlendirmesi (0-100%)

#### Güvenlik Analizi
- **WPS Tespiti**: WPS etkin ağlar (güvenlik riski)
- **RSN IE Analizi**: WPA2/WPA3 protokol tespiti
- **PMKID Tespiti**: Pasif PMKID yakalama
- **EAPOL Frame Tespiti**: Handshake fragment tespiti
- **Cipher Suite Analizi**: CCMP, TKIP tespiti
- **AKM Suite Analizi**: PSK, SAE, FT-PSK tespiti

### 📊 Analiz ve Raporlama

#### Canlı Grafikler
- **RSSI Zaman Grafiği**: Gradient fill efektli, modern tasarım
- **Kanal Yoğunluk Heatmap**: Renkli bar grafikleri, değer etiketleri
- **Frame Trafik Grafiği**: Gerçek zamanlı trafik analizi
- **SNR Analizi Tablosu**: Detaylı SNR karşılaştırması

#### Raporlama
- **PDF Raporlar**: Profesyonel, çok sayfalı raporlar
- **HTML Raporlar**: Modern, responsive tasarım, interaktif tablolar
- **CSV Export**: Veri analizi için dışa aktarım

### 🎨 Modern Kullanıcı Arayüzü

#### Ultra Modern Tasarım
- **Gradient Renkler**: Indigo/Purple modern renk paleti
- **İkonlar**: Tüm sekmeler ve özelliklerde emoji ikonlar
- **Glassmorphism**: Modern cam efekti tasarım
- **Hover Efektleri**: İnteraktif buton ve elementler
- **Risk Badge'leri**: Renkli risk skoru gösterimi
- **Modern Tipografi**: Inter font ailesi, hiyerarşik font boyutları

#### Ana Ekran Özellikleri
- **Modern Header**: Stats ile birlikte (Toplam/Filtrelenmiş ağ sayısı)
- **Gelişmiş Filtreler**: Üretici, Bant, Güvenlik, RSSI filtreleme
- **Renkli Tablo**: Risk skoruna göre renklendirilmiş satırlar
- **Detay Paneli**: Sağdan açılan, sekmeli detay görüntüleme
  - 📋 Genel Bilgi: SSID, BSSID, Vendor, Kanal, RSSI, Güvenlik
  - 🔒 Güvenlik Analizi: Detaylı protokol bilgisi, Risk skoru, Evil Twin riski
  - 👥 Bağlı Cihazlar: Client MAC, Vendor, RSSI, Device Type, Frame Count
  - 📈 Canlı Grafikler: RSSI zaman grafiği, Kanal heatmap
  - 🚨 Güvenlik Olayları: IDS olayları, zaman damgalı kayıtlar

#### Sekmeler
- 🏠 **Ana Ekran**: Ağ listesi, filtreler, detay paneli
- 📈 **Canlı Grafikler**: RSSI, Kanal heatmap, Trafik grafikleri
- 🔒 **Güvenlik**: SNR analizi, Overlap matrisi, Güvenlik önerileri
- 🚨 **IDS Olayları**: Tespit edilen saldırılar, olay detayları
- 📄 **Raporlar**: PDF, HTML, CSV rapor oluşturma
- ⚙️ **Ayarlar**: Interface, kanal, yenileme ayarları

---

## 🛠️ Teknolojiler

### Programlama Dili
- **Python 3.11+**: Ana programlama dili

### Kütüphaneler ve Framework'ler

#### Core Libraries
- **Scapy 2.5.1+**: Paket yakalama ve analiz
- **manuf 1.1.5+**: MAC adresi üretici tespiti
- **SQLite3**: Veritabanı (WAL mode, thread-safe)
- **Pandas 2.2.0+**: Veri analizi
- **NumPy 1.24.0+**: Sayısal hesaplamalar

#### GUI Libraries
- **Tkinter**: GUI framework (Python built-in)
- **ttk**: Modern widget'lar
- **Matplotlib 3.7.2+**: Grafik oluşturma (gradient fill, modern styling)

#### Raporlama
- **ReportLab 4.1.0+**: PDF rapor oluşturma
- **Jinja2 3.1.2+**: HTML template engine
- **Pillow 9.5.0+**: Görsel işleme

#### Testing
- **pytest 7.3.0+**: Test framework
- **pytest-cov 4.1.0+**: Test coverage

### Sistem Araçları
- **iw**: Wireless interface yönetimi
- **airmon-ng**: Monitor mode yönetimi (Kali Linux)

---

## 📦 Kurulum

### Gereksinimler

- **İşletim Sistemi**: Kali Linux (önerilen) veya Linux dağıtımları
- **Python**: 3.11 veya üzeri
- **Wireless Interface**: Monitor mode destekleyen WiFi adaptörü
- **Root/Sudo**: Monitor mode için gerekli

### Adım 1: Repository'yi Klonlayın

```bash
git clone <repository-url>
cd wifi_scanner_project
```

### Adım 2: Python Sanal Ortamı Oluşturun

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Adım 4: Monitor Mode'u Aktifleştirin

```bash
# WiFi interface'inizi bulun
iwconfig

# Monitor mode'u aktifleştirin
sudo airmon-ng start wlan0

# veya manuel olarak
sudo iw dev wlan0 set type monitor
sudo ifconfig wlan0mon up
```

### Adım 5: Uygulamayı Çalıştırın

```bash
sudo python3 main.py
```

**Not**: Monitor mode için root/sudo yetkisi gereklidir.

---

## 🚀 Kullanım

### Temel Kullanım

1. **Uygulamayı Başlatın**: `sudo python3 main.py`
2. **Ana Ekranda**: Çevredeki WiFi ağları otomatik olarak tespit edilir
3. **Filtreleme**: Üretici, bant, güvenlik, RSSI filtrelerini kullanın
4. **Detay Görüntüleme**: 
   - Çift tıklayın
   - Sağ tık → "Detaylı Analiz"
   - Enter tuşuna basın
5. **Rapor Oluşturma**: Raporlar sekmesinden PDF/HTML/CSV oluşturun

### Gelişmiş Özellikler

#### Risk Skoru Analizi
- Her ağ için otomatik risk skoru hesaplanır (0-100%)
- Risk skoruna göre renklendirilmiş satırlar
- Detay panelinde detaylı risk analizi

#### Client-AP İlişkisi
- Data frame'ler otomatik analiz edilir
- Hangi cihazın hangi AP'ye bağlı olduğu görüntülenir
- Client vendor ve device type bilgisi

#### IDS Olayları
- Gerçek zamanlı saldırı tespiti
- IDS Olayları sekmesinde görüntüleme
- Zaman damgalı kayıtlar

---

## 📁 Proje Yapısı

```
wifi_scanner_project/
├── core/                    # Ana analiz modülleri
│   ├── scanner.py          # WiFi paket yakalama ve analiz
│   ├── security_analyzer.py # Güvenlik protokolü analizi
│   ├── ids_engine.py       # IDS motoru
│   ├── rogue_ap_detector.py # Rogue AP tespiti
│   ├── risk_calculator.py  # Risk skoru hesaplama
│   ├── mac_profiler.py     # Vendor ve device type tespiti
│   ├── channel_analyzer.py # Kanal analizi
│   ├── snr_analyzer.py     # SNR analizi
│   └── ml/                 # ML modülleri (placeholder)
├── gui/                    # Kullanıcı arayüzü
│   ├── gui_main.py         # Ana GUI
│   ├── detail_panel.py     # Detay paneli
│   ├── live_graphs.py      # Canlı grafikler
│   ├── styles.py           # Modern stil tanımları
│   └── popup.py            # Bildirimler
├── reports/                # Rapor oluşturma
│   ├── pdf_report.py       # PDF rapor
│   ├── html_report.py      # HTML rapor
│   └── csv_export.py       # CSV export
├── utils/                  # Yardımcı fonksiyonlar
│   ├── db.py              # Veritabanı yönetimi
│   ├── logger.py          # Logging
│   ├── config_manager.py  # Konfigürasyon
│   └── threads.py         # Thread yönetimi
├── tests/                  # Test dosyaları
├── data/                   # Veritabanı ve loglar
├── config.ini             # Konfigürasyon dosyası
├── requirements.txt       # Python bağımlılıkları
├── main.py               # Ana giriş noktası
├── README.md             # Bu dosya
└── PROJE_RAPORU.md       # Proje raporu
```

---

## 🔧 Modüller ve Bileşenler

### Core Modülleri

#### `scanner.py` - WiFi Scanner
- Pasif paket yakalama (Scapy)
- Beacon, Probe Request, Data frame işleme
- Detaylı güvenlik protokolü analizi
- Client-AP ilişkisi tespiti
- Otomatik kanal atlama

#### `security_analyzer.py` - Güvenlik Analizi
- WPS tespiti
- RSN IE analizi
- Güvenlik önerileri

#### `ids_engine.py` - IDS Motoru
- Deauth flood tespiti
- Probe storm tespiti
- Beacon flood tespiti
- Association flood tespiti
- MAC spoofing tespiti

#### `rogue_ap_detector.py` - Rogue AP Tespiti
- Evil twin tespiti
- Vendor uyumsuzluğu
- Güvenlik protokolü farklılığı
- Risk skoru hesaplama

#### `risk_calculator.py` - Risk Skoru Hesaplama
- Güvenlik protokolü riski
- WPS riski
- PMF riski
- Evil twin riski
- Yüzdesel risk skoru (0-100%)

#### `mac_profiler.py` - Vendor ve Device Type Tespiti
- manuf kütüphanesi entegrasyonu
- OUI veritabanı fallback
- Device type tespiti (Telefon, Laptop, Router)

#### `channel_analyzer.py` - Kanal Analizi
- Kanal yoğunluk analizi
- Overlap matrisi hesaplama
- DFS kanal tespiti
- En iyi kanal önerisi

#### `snr_analyzer.py` - SNR Analizi
- SNR hesaplama
- Noise floor tespiti
- Ağ bazlı SNR analizi

### GUI Modülleri

#### `gui_main.py` - Ana GUI
- Ultra modern, sekmeli arayüz
- Gelişmiş filtreleme sistemi
- Canlı veri güncelleme
- Detay paneli entegrasyonu
- Risk skoru gösterimi

#### `detail_panel.py` - Detay Paneli
- Sağdan açılan modern panel
- 5 sekme: Genel, Güvenlik, Bağlı Cihazlar, Grafikler, Olaylar
- Gerçek zamanlı veri güncelleme

#### `live_graphs.py` - Canlı Grafikler
- Modern gradient fill efektli grafikler
- RSSI zaman grafiği
- Kanal heatmap
- Trafik grafiği

#### `styles.py` - Modern Stil Tanımları
- Ultra modern renk paleti
- Gradient renkler
- Modern tipografi
- Hover efektleri

### Rapor Modülleri

#### `pdf_report.py` - PDF Rapor
- Profesyonel PDF oluşturma
- Tablolar ve grafikler
- Çok sayfalı raporlar

#### `html_report.py` - HTML Rapor
- Modern, responsive tasarım
- Interaktif tablolar
- CSS stillendirme

#### `csv_export.py` - CSV Export
- Veri analizi için dışa aktarım
- Excel uyumlu format

---

## 🧪 Test

### Tüm Testleri Çalıştır

```bash
pytest tests/ -v
```

### Belirli Test Dosyası

```bash
pytest tests/test_scanner.py -v
pytest tests/test_ids.py -v
pytest tests/test_security.py -v
pytest tests/test_gui.py -v
```

### Entegrasyon Testi

```bash
python3 tests/selftest.py
```

### Test Kapsamı

- ✅ Veritabanı migration testleri
- ✅ Scanner başlatma testleri
- ✅ IDS tespit testleri
- ✅ Güvenlik analiz testleri
- ✅ GUI başlatma testleri
- ✅ Filtreleme testleri
- ✅ Risk skoru hesaplama testleri
- ✅ Vendor tespiti testleri

---

## 📸 Ekran Görüntüleri

### Ana Ekran
- Modern header ile stats gösterimi
- Renkli risk badge'leri
- Gelişmiş filtreleme paneli
- Detay paneli entegrasyonu

### Canlı Grafikler
- Gradient fill efektli RSSI grafiği
- Modern kanal heatmap
- Frame trafik grafiği

### Güvenlik Sekmesi
- SNR analizi tablosu
- Kanal overlap matrisi
- Güvenlik önerileri

### Detay Paneli
- 5 sekmeli modern panel
- Genel bilgi, güvenlik analizi, bağlı cihazlar
- Canlı grafikler ve güvenlik olayları

### IDS Olayları
- Tespit edilen saldırılar
- Olay detayları
- Zaman damgalı kayıtlar

---

## ⚠️ Etik Kullanım ve Yasal Uyarı

### ✅ İzin Verilen Kullanımlar

- Kendi ağlarınızı analiz etmek
- Yetkili olduğunuz ağları test etmek
- Eğitim ve araştırma amaçlı kullanım
- Güvenlik farkındalığı oluşturmak

### ❌ Yasak Kullanımlar

- Yetkisiz ağlara müdahale etmek
- Saldırı amaçlı kullanım
- Kişisel verileri toplamak
- Yasalara aykırı aktiviteler

### Yasal Sorumluluk

Bu araç **sadece eğitim ve güvenlik araştırması** amaçlıdır. Kullanımından **kullanıcı sorumludur**. Yetkisiz ağ analizi ve müdahale yasalara aykırıdır ve cezai yaptırımlara tabidir.

**ÖNEMLİ**: Bu proje tamamen **pasif analiz** prensibine dayanır. Hiçbir paket gönderilmez veya ağa müdahale edilmez.

---

## 🚀 Gelecek Geliştirmeler

### Planlanan Özellikler

- [ ] Makine öğrenimi ile cihaz sınıflandırma
- [ ] Anomali tespiti (Isolation Forest)
- [ ] LSTM tabanlı hareket analizi
- [ ] Web arayüzü (FastAPI)
- [ ] Veritabanı şifreleme
- [ ] Çoklu dil desteği
- [ ] Tray icon ve sistem bildirimleri
- [ ] Topoloji haritası görselleştirmesi

### ML Modülleri

Mevcut ML modülleri placeholder olarak hazırlanmıştır:
- `anomaly_detector.py`
- `device_classifier.py`
- `traffic_ml_engine.py`
- `movement_lstm.py`
- `heatmap_model.py`

---

## 📚 Kaynaklar

### Dokümantasyon
- [Scapy Documentation](https://scapy.readthedocs.io/)
- [Python Tkinter Guide](https://docs.python.org/3/library/tkinter.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [manuf Documentation](https://github.com/coolbho3k/manuf)

### Referanslar
- IEEE 802.11 Standard
- WiFi Security Best Practices
- Passive Network Analysis Techniques

### Eğitim Materyalleri
- Wireless Security Fundamentals
- Network Packet Analysis
- Ethical Hacking Principles

---

## 👨‍💻 Geliştirici

**Musa Yoncalık**

Bu proje, bitirme projesi kapsamında geliştirilmiştir. Tüm kodlar eğitim amaçlıdır ve etik kullanım prensiplerine uygun olarak tasarlanmıştır.

---

## 📄 Lisans

Bu proje eğitim amaçlıdır. Kullanımından kullanıcı sorumludur.

---

## 🙏 Teşekkürler

- Scapy geliştiricilerine
- manuf kütüphanesi geliştiricilerine
- Python topluluğuna
- Açık kaynak topluluğuna

---

**Son Güncelleme:** 2024  
**Versiyon:** 2.0  
**Durum:** ✅ Production Ready - Ultra Modern Tasarım

**Platform:** Kali Linux  
**Versiyon:** 2.0  
**Durum:** ✅ Tamamlandı - Production Ready

---

## 📋 İçindekiler

1. [Proje Özeti](#proje-özeti)
2. [Proje Amacı](#proje-amacı)
3. [Özellikler](#özellikler)
4. [Teknolojiler](#teknolojiler)
5. [Kurulum](#kurulum)
6. [Kullanım](#kullanım)
7. [Proje Yapısı](#proje-yapısı)
8. [Modüller ve Bileşenler](#modüller-ve-bileşenler)
9. [Test](#test)
10. [Ekran Görüntüleri](#ekran-görüntüleri)
11. [Etik Kullanım ve Yasal Uyarı](#etik-kullanım-ve-yasal-uyarı)
12. [Gelecek Geliştirmeler](#gelecek-geliştirmeler)
13. [Kaynaklar](#kaynaklar)

---

## 🎯 Proje Özeti

**WiFi Scanner Pro**, Kali Linux üzerinde çalışan, tamamen **pasif analiz prensibine dayalı**, ultra modern ve profesyonel bir masaüstü uygulamasıdır. Proje, çevredeki Wi-Fi ağlarını gerçek zamanlı olarak analiz etmek, detaylı güvenlik değerlendirmesi yapmak ve kullanıcıda ağ güvenliği konusunda farkındalık oluşturmak amacıyla geliştirilmiştir.

### ✨ Temel Özellikler

- ✅ **Tamamen Pasif Analiz**: Hiçbir paket gönderilmez, sadece dinleme yapılır
- ✅ **Gerçek Zamanlı İzleme**: Canlı grafikler ve anlık güncellemeler
- ✅ **Gelişmiş IDS**: Saldırı tespiti ve güvenlik analizi
- ✅ **Profesyonel Raporlama**: PDF, HTML ve CSV formatlarında raporlar
- ✅ **Ultra Modern GUI**: Gradient renkler, ikonlar, glassmorphism efektleri
- ✅ **Detaylı Güvenlik Analizi**: WPA2-PSK (CCMP), WPA3-SAE, WPS, PMF tespiti
- ✅ **Vendor Tespiti**: manuf kütüphanesi ile gerçek üretici bilgisi
- ✅ **Client-AP İlişkisi**: Data frame analizi ile bağlı cihaz tespiti
- ✅ **Risk Skoru Hesaplama**: Yüzdesel risk değerlendirmesi
- ✅ **Detay Paneli**: Sağdan açılan, sekmeli detay görüntüleme

---

## 🎓 Proje Amacı

Bu proje, özellikle teknik bilgisi sınırlı kullanıcıların dahi Wi-Fi ortamlarını anlayabilmesini ve olası riskleri fark edebilmesini hedefler. Uygulama:

- Kablosuz ağlardan yayılan paketleri **pasif olarak** dinleyerek analiz eder
- Ağ adı (SSID), MAC adresi (BSSID), sinyal gücü (RSSI), kanal bilgisi ve **detaylı güvenlik protokollerini** tespit eder
- Bu verileri güvenlik, performans ve IDS modülleri ile analiz eder
- Elde edilen sonuçları **modern grafikler** ve detaylı raporlar halinde kullanıcıya sunar
- **Saldırı veya ağa müdahale içermeyen** yapısıyla etik ve yasal sınırlar içinde kalır

---

## ✨ Özellikler

### 🔍 Temel Analiz Özellikleri

#### Pasif WiFi Tarama
- Monitor mode'da paket yakalama (Scapy)
- Otomatik kanal atlama (2.4GHz ve 5GHz)
- Beacon, Probe Request ve **Data frame** analizi
- Gerçek zamanlı ağ keşfi
- Multi-threaded paket işleme

#### Ağ Bilgisi Çıkarımı
- **SSID**: Ağ adı tespiti (Hidden ağ desteği)
- **BSSID**: MAC adresi
- **Kanal**: 2.4GHz ve 5GHz kanal bilgisi
- **RSSI**: Sinyal gücü ölçümü (dBm)
- **Güvenlik Protokolü**: Detaylı tespit (WPA2-PSK (CCMP), WPA3-SAE, WEP, Open)
- **Vendor Bilgisi**: manuf kütüphanesi ile gerçek üretici tespiti (Apple, Samsung, TP-Link, vb.)
- **Risk Skoru**: Yüzdesel risk değerlendirmesi (0-100%)

#### Detaylı Güvenlik Analizi
- **WPA2-PSK (CCMP)**: Güçlü şifreleme tespiti
- **WPA2-PSK (TKIP)**: Zayıf şifreleme uyarısı
- **WPA3-SAE**: En güvenli protokol
- **WPS Durumu**: WPS açık/kapalı tespiti
- **PMF (Protected Management Frames)**: PMF zorunlu/destekli tespiti
- **WEP**: Güvensiz protokol uyarısı
- **Open Network**: Şifreleme yok uyarısı

#### Client-AP İlişkisi Tespiti
- **Data Frame Analizi**: Hangi cihazın hangi AP'ye bağlı olduğunu tespit
- **Client MAC**: Bağlı cihaz MAC adresleri
- **Vendor Tespiti**: Client cihaz üretici bilgisi
- **Device Type**: Telefon, Laptop, Router tespiti
- **Frame Count**: Trafik analizi
- **RSSI Tracking**: Client sinyal gücü takibi

#### SNR ve Performans Analizi
- **SNR Hesaplama**: Signal-to-Noise Ratio analizi
- **Noise Floor**: Gürültü seviyesi tespiti
- **Kanal Overlap Matrisi**: Kanal girişim analizi
- **DFS Desteği**: 5GHz radar bantları tespiti
- **En İyi Kanal Önerisi**: Otomatik kanal optimizasyonu

### 🛡️ Güvenlik Özellikleri

#### IDS (Intrusion Detection System)
- **Deauth Flood Tespiti**: Deauthentication saldırıları
- **Probe Storm Tespiti**: Probe request fırtınaları
- **Beacon Flood Tespiti**: Beacon frame saldırıları
- **Association Flood Tespiti**: Association request saldırıları
- **MAC Spoofing Tespiti**: Şüpheli MAC adresi aktiviteleri
- **Gerçek Zamanlı Uyarılar**: Anlık saldırı bildirimleri

#### Rogue AP Tespiti
- **Evil Twin Tespiti**: Aynı SSID'ye sahip sahte erişim noktaları
- **Vendor Uyumsuzluğu**: Farklı üreticilerden aynı SSID
- **Güvenlik Protokolü Farklılığı**: Open vs şifreli ağ tespiti
- **Kanal Yakınlığı**: Şüpheli kanal dağılımı
- **Risk Skoru Hesaplama**: Yüzdesel risk değerlendirmesi (0-100%)

#### Güvenlik Analizi
- **WPS Tespiti**: WPS etkin ağlar (güvenlik riski)
- **RSN IE Analizi**: WPA2/WPA3 protokol tespiti
- **PMKID Tespiti**: Pasif PMKID yakalama
- **EAPOL Frame Tespiti**: Handshake fragment tespiti
- **Cipher Suite Analizi**: CCMP, TKIP tespiti
- **AKM Suite Analizi**: PSK, SAE, FT-PSK tespiti

### 📊 Analiz ve Raporlama

#### Canlı Grafikler
- **RSSI Zaman Grafiği**: Gradient fill efektli, modern tasarım
- **Kanal Yoğunluk Heatmap**: Renkli bar grafikleri, değer etiketleri
- **Frame Trafik Grafiği**: Gerçek zamanlı trafik analizi
- **SNR Analizi Tablosu**: Detaylı SNR karşılaştırması

#### Raporlama
- **PDF Raporlar**: Profesyonel, çok sayfalı raporlar
- **HTML Raporlar**: Modern, responsive tasarım, interaktif tablolar
- **CSV Export**: Veri analizi için dışa aktarım

### 🎨 Modern Kullanıcı Arayüzü

#### Ultra Modern Tasarım
- **Gradient Renkler**: Indigo/Purple modern renk paleti
- **İkonlar**: Tüm sekmeler ve özelliklerde emoji ikonlar
- **Glassmorphism**: Modern cam efekti tasarım
- **Hover Efektleri**: İnteraktif buton ve elementler
- **Risk Badge'leri**: Renkli risk skoru gösterimi
- **Modern Tipografi**: Inter font ailesi, hiyerarşik font boyutları

#### Ana Ekran Özellikleri
- **Modern Header**: Stats ile birlikte (Toplam/Filtrelenmiş ağ sayısı)
- **Gelişmiş Filtreler**: Üretici, Bant, Güvenlik, RSSI filtreleme
- **Renkli Tablo**: Risk skoruna göre renklendirilmiş satırlar
- **Detay Paneli**: Sağdan açılan, sekmeli detay görüntüleme
  - 📋 Genel Bilgi: SSID, BSSID, Vendor, Kanal, RSSI, Güvenlik
  - 🔒 Güvenlik Analizi: Detaylı protokol bilgisi, Risk skoru, Evil Twin riski
  - 👥 Bağlı Cihazlar: Client MAC, Vendor, RSSI, Device Type, Frame Count
  - 📈 Canlı Grafikler: RSSI zaman grafiği, Kanal heatmap
  - 🚨 Güvenlik Olayları: IDS olayları, zaman damgalı kayıtlar

#### Sekmeler
- 🏠 **Ana Ekran**: Ağ listesi, filtreler, detay paneli
- 📈 **Canlı Grafikler**: RSSI, Kanal heatmap, Trafik grafikleri
- 🔒 **Güvenlik**: SNR analizi, Overlap matrisi, Güvenlik önerileri
- 🚨 **IDS Olayları**: Tespit edilen saldırılar, olay detayları
- 📄 **Raporlar**: PDF, HTML, CSV rapor oluşturma
- ⚙️ **Ayarlar**: Interface, kanal, yenileme ayarları

---

## 🛠️ Teknolojiler

### Programlama Dili
- **Python 3.11+**: Ana programlama dili

### Kütüphaneler ve Framework'ler

#### Core Libraries
- **Scapy 2.5.1+**: Paket yakalama ve analiz
- **manuf 1.1.5+**: MAC adresi üretici tespiti
- **SQLite3**: Veritabanı (WAL mode, thread-safe)
- **Pandas 2.2.0+**: Veri analizi
- **NumPy 1.24.0+**: Sayısal hesaplamalar

#### GUI Libraries
- **Tkinter**: GUI framework (Python built-in)
- **ttk**: Modern widget'lar
- **Matplotlib 3.7.2+**: Grafik oluşturma (gradient fill, modern styling)

#### Raporlama
- **ReportLab 4.1.0+**: PDF rapor oluşturma
- **Jinja2 3.1.2+**: HTML template engine
- **Pillow 9.5.0+**: Görsel işleme

#### Testing
- **pytest 7.3.0+**: Test framework
- **pytest-cov 4.1.0+**: Test coverage

### Sistem Araçları
- **iw**: Wireless interface yönetimi
- **airmon-ng**: Monitor mode yönetimi (Kali Linux)

---

## 📦 Kurulum

### Gereksinimler

- **İşletim Sistemi**: Kali Linux (önerilen) veya Linux dağıtımları
- **Python**: 3.11 veya üzeri
- **Wireless Interface**: Monitor mode destekleyen WiFi adaptörü
- **Root/Sudo**: Monitor mode için gerekli

### Adım 1: Repository'yi Klonlayın

```bash
git clone <repository-url>
cd wifi_scanner_project
```

### Adım 2: Python Sanal Ortamı Oluşturun

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Adım 4: Monitor Mode'u Aktifleştirin

```bash
# WiFi interface'inizi bulun
iwconfig

# Monitor mode'u aktifleştirin
sudo airmon-ng start wlan0

# veya manuel olarak
sudo iw dev wlan0 set type monitor
sudo ifconfig wlan0mon up
```

### Adım 5: Uygulamayı Çalıştırın

```bash
sudo python3 main.py
```

**Not**: Monitor mode için root/sudo yetkisi gereklidir.

---

## 🚀 Kullanım

### Temel Kullanım

1. **Uygulamayı Başlatın**: `sudo python3 main.py`
2. **Ana Ekranda**: Çevredeki WiFi ağları otomatik olarak tespit edilir
3. **Filtreleme**: Üretici, bant, güvenlik, RSSI filtrelerini kullanın
4. **Detay Görüntüleme**: 
   - Çift tıklayın
   - Sağ tık → "Detaylı Analiz"
   - Enter tuşuna basın
5. **Rapor Oluşturma**: Raporlar sekmesinden PDF/HTML/CSV oluşturun

### Gelişmiş Özellikler

#### Risk Skoru Analizi
- Her ağ için otomatik risk skoru hesaplanır (0-100%)
- Risk skoruna göre renklendirilmiş satırlar
- Detay panelinde detaylı risk analizi

#### Client-AP İlişkisi
- Data frame'ler otomatik analiz edilir
- Hangi cihazın hangi AP'ye bağlı olduğu görüntülenir
- Client vendor ve device type bilgisi

#### IDS Olayları
- Gerçek zamanlı saldırı tespiti
- IDS Olayları sekmesinde görüntüleme
- Zaman damgalı kayıtlar

---

## 📁 Proje Yapısı

```
wifi_scanner_project/
├── core/                    # Ana analiz modülleri
│   ├── scanner.py          # WiFi paket yakalama ve analiz
│   ├── security_analyzer.py # Güvenlik protokolü analizi
│   ├── ids_engine.py       # IDS motoru
│   ├── rogue_ap_detector.py # Rogue AP tespiti
│   ├── risk_calculator.py  # Risk skoru hesaplama
│   ├── mac_profiler.py     # Vendor ve device type tespiti
│   ├── channel_analyzer.py # Kanal analizi
│   ├── snr_analyzer.py     # SNR analizi
│   └── ml/                 # ML modülleri (placeholder)
├── gui/                    # Kullanıcı arayüzü
│   ├── gui_main.py         # Ana GUI
│   ├── detail_panel.py     # Detay paneli
│   ├── live_graphs.py      # Canlı grafikler
│   ├── styles.py           # Modern stil tanımları
│   └── popup.py            # Bildirimler
├── reports/                # Rapor oluşturma
│   ├── pdf_report.py       # PDF rapor
│   ├── html_report.py      # HTML rapor
│   └── csv_export.py       # CSV export
├── utils/                  # Yardımcı fonksiyonlar
│   ├── db.py              # Veritabanı yönetimi
│   ├── logger.py          # Logging
│   ├── config_manager.py  # Konfigürasyon
│   └── threads.py         # Thread yönetimi
├── tests/                  # Test dosyaları
├── data/                   # Veritabanı ve loglar
├── config.ini             # Konfigürasyon dosyası
├── requirements.txt       # Python bağımlılıkları
├── main.py               # Ana giriş noktası
├── README.md             # Bu dosya
└── PROJE_RAPORU.md       # Proje raporu
```

---

## 🔧 Modüller ve Bileşenler

### Core Modülleri

#### `scanner.py` - WiFi Scanner
- Pasif paket yakalama (Scapy)
- Beacon, Probe Request, Data frame işleme
- Detaylı güvenlik protokolü analizi
- Client-AP ilişkisi tespiti
- Otomatik kanal atlama

#### `security_analyzer.py` - Güvenlik Analizi
- WPS tespiti
- RSN IE analizi
- Güvenlik önerileri

#### `ids_engine.py` - IDS Motoru
- Deauth flood tespiti
- Probe storm tespiti
- Beacon flood tespiti
- Association flood tespiti
- MAC spoofing tespiti

#### `rogue_ap_detector.py` - Rogue AP Tespiti
- Evil twin tespiti
- Vendor uyumsuzluğu
- Güvenlik protokolü farklılığı
- Risk skoru hesaplama

#### `risk_calculator.py` - Risk Skoru Hesaplama
- Güvenlik protokolü riski
- WPS riski
- PMF riski
- Evil twin riski
- Yüzdesel risk skoru (0-100%)

#### `mac_profiler.py` - Vendor ve Device Type Tespiti
- manuf kütüphanesi entegrasyonu
- OUI veritabanı fallback
- Device type tespiti (Telefon, Laptop, Router)

#### `channel_analyzer.py` - Kanal Analizi
- Kanal yoğunluk analizi
- Overlap matrisi hesaplama
- DFS kanal tespiti
- En iyi kanal önerisi

#### `snr_analyzer.py` - SNR Analizi
- SNR hesaplama
- Noise floor tespiti
- Ağ bazlı SNR analizi

### GUI Modülleri

#### `gui_main.py` - Ana GUI
- Ultra modern, sekmeli arayüz
- Gelişmiş filtreleme sistemi
- Canlı veri güncelleme
- Detay paneli entegrasyonu
- Risk skoru gösterimi

#### `detail_panel.py` - Detay Paneli
- Sağdan açılan modern panel
- 5 sekme: Genel, Güvenlik, Bağlı Cihazlar, Grafikler, Olaylar
- Gerçek zamanlı veri güncelleme

#### `live_graphs.py` - Canlı Grafikler
- Modern gradient fill efektli grafikler
- RSSI zaman grafiği
- Kanal heatmap
- Trafik grafiği

#### `styles.py` - Modern Stil Tanımları
- Ultra modern renk paleti
- Gradient renkler
- Modern tipografi
- Hover efektleri

### Rapor Modülleri

#### `pdf_report.py` - PDF Rapor
- Profesyonel PDF oluşturma
- Tablolar ve grafikler
- Çok sayfalı raporlar

#### `html_report.py` - HTML Rapor
- Modern, responsive tasarım
- Interaktif tablolar
- CSS stillendirme

#### `csv_export.py` - CSV Export
- Veri analizi için dışa aktarım
- Excel uyumlu format

---

## 🧪 Test

### Tüm Testleri Çalıştır

```bash
pytest tests/ -v
```

### Belirli Test Dosyası

```bash
pytest tests/test_scanner.py -v
pytest tests/test_ids.py -v
pytest tests/test_security.py -v
pytest tests/test_gui.py -v
```

### Entegrasyon Testi

```bash
python3 tests/selftest.py
```

### Test Kapsamı

- ✅ Veritabanı migration testleri
- ✅ Scanner başlatma testleri
- ✅ IDS tespit testleri
- ✅ Güvenlik analiz testleri
- ✅ GUI başlatma testleri
- ✅ Filtreleme testleri
- ✅ Risk skoru hesaplama testleri
- ✅ Vendor tespiti testleri

---

## 📸 Ekran Görüntüleri

### Ana Ekran
- Modern header ile stats gösterimi
- Renkli risk badge'leri
- Gelişmiş filtreleme paneli
- Detay paneli entegrasyonu

### Canlı Grafikler
- Gradient fill efektli RSSI grafiği
- Modern kanal heatmap
- Frame trafik grafiği

### Güvenlik Sekmesi
- SNR analizi tablosu
- Kanal overlap matrisi
- Güvenlik önerileri

### Detay Paneli
- 5 sekmeli modern panel
- Genel bilgi, güvenlik analizi, bağlı cihazlar
- Canlı grafikler ve güvenlik olayları

### IDS Olayları
- Tespit edilen saldırılar
- Olay detayları
- Zaman damgalı kayıtlar

---

## ⚠️ Etik Kullanım ve Yasal Uyarı

### ✅ İzin Verilen Kullanımlar

- Kendi ağlarınızı analiz etmek
- Yetkili olduğunuz ağları test etmek
- Eğitim ve araştırma amaçlı kullanım
- Güvenlik farkındalığı oluşturmak

### ❌ Yasak Kullanımlar

- Yetkisiz ağlara müdahale etmek
- Saldırı amaçlı kullanım
- Kişisel verileri toplamak
- Yasalara aykırı aktiviteler

### Yasal Sorumluluk

Bu araç **sadece eğitim ve güvenlik araştırması** amaçlıdır. Kullanımından **kullanıcı sorumludur**. Yetkisiz ağ analizi ve müdahale yasalara aykırıdır ve cezai yaptırımlara tabidir.

**ÖNEMLİ**: Bu proje tamamen **pasif analiz** prensibine dayanır. Hiçbir paket gönderilmez veya ağa müdahale edilmez.

---

## 🚀 Gelecek Geliştirmeler

### Planlanan Özellikler

- [ ] Makine öğrenimi ile cihaz sınıflandırma
- [ ] Anomali tespiti (Isolation Forest)
- [ ] LSTM tabanlı hareket analizi
- [ ] Web arayüzü (FastAPI)
- [ ] Veritabanı şifreleme
- [ ] Çoklu dil desteği
- [ ] Tray icon ve sistem bildirimleri
- [ ] Topoloji haritası görselleştirmesi

### ML Modülleri

Mevcut ML modülleri placeholder olarak hazırlanmıştır:
- `anomaly_detector.py`
- `device_classifier.py`
- `traffic_ml_engine.py`
- `movement_lstm.py`
- `heatmap_model.py`

---

## 📚 Kaynaklar

### Dokümantasyon
- [Scapy Documentation](https://scapy.readthedocs.io/)
- [Python Tkinter Guide](https://docs.python.org/3/library/tkinter.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [manuf Documentation](https://github.com/coolbho3k/manuf)

### Referanslar
- IEEE 802.11 Standard
- WiFi Security Best Practices
- Passive Network Analysis Techniques

### Eğitim Materyalleri
- Wireless Security Fundamentals
- Network Packet Analysis
- Ethical Hacking Principles

---

## 👨‍💻 Geliştirici

**Musa Yoncalık**

Bu proje, bitirme projesi kapsamında geliştirilmiştir. Tüm kodlar eğitim amaçlıdır ve etik kullanım prensiplerine uygun olarak tasarlanmıştır.

---

## 📄 Lisans

Bu proje eğitim amaçlıdır. Kullanımından kullanıcı sorumludur.

---

## 🙏 Teşekkürler

- Scapy geliştiricilerine
- manuf kütüphanesi geliştiricilerine
- Python topluluğuna
- Açık kaynak topluluğuna

---

**Son Güncelleme:** 2025 
**Versiyon:** 2.0  
**Durum:** ✅ Production Ready - Ultra Modern Tasarım
