# WiFi Scanner Pro

## Pasif WiFi Analiz ve Güvenlik Değerlendirme Aracı

**Öğrenci:** Musa Yoncalık
**Tarih:** 2025
**Versiyon:** 2.0
**Durum:** ✅ Tamamlandı – Production Ready

---

## 1. Proje Özeti

**WiFi Scanner Pro**, Kali Linux üzerinde çalışan, tamamen **pasif analiz prensibine dayalı**, profesyonel bir WiFi analiz ve güvenlik değerlendirme aracıdır. Proje; çevredeki kablosuz ağları gerçek zamanlı olarak analiz etmeyi, güvenlik yapılandırmalarını derinlemesine incelemeyi ve kullanıcıda ağ güvenliği farkındalığı oluşturmayı amaçlamaktadır.

Uygulama hiçbir şekilde ağa paket göndermez; yalnızca havada yayınlanan 802.11 çerçevelerini dinler. Bu yaklaşım sayesinde etik ve yasal sınırlar içinde, tespit edilmeden analiz yapılabilmektedir.

---

## 2. Projenin Amacı ve Kapsamı

### 2.1 Projenin Amacı

Bu projenin temel amacı, standart WiFi tarama araçlarının ötesine geçerek:

* Gizli (Hidden) ağları ve pasif trafiği görünür kılmak
* Sadece şifreleme türünü değil, **konfigürasyon zafiyetlerini** (WPS, eski cipher’lar, PMF eksikliği) analiz etmek
* Yetkisiz erişim denemeleri ve sahte erişim noktalarını (Rogue AP) tespit etmek
* Kullanıcıya teknik ama anlaşılır bir **“Güvenlik Röntgeni”** sunmaktır

Aynı zamanda proje, geliştiricinin ağ protokolleri, Python ile eşzamanlı programlama ve gerçek zamanlı GUI geliştirme konularındaki bilgisini pratik bir mühendislik ürününe dönüştürmesini hedeflemiştir.

---

### 2.2 Standart WiFi Tarama Araçlarından Farkı

| Kriter             | Standart Cihazlar      | WiFi Scanner Pro      |
| ------------------ | ---------------------- | --------------------- |
| Tarama Türü        | Aktif (Probe gönderir) | Tamamen Pasif         |
| Görünürlük         | Sadece AP              | AP + Client + Trafik  |
| Gizli Ağlar        | Görünmez               | Tespit Edilir         |
| Güvenlik Derinliği | Yüzeysel               | Cipher, AKM, PMF, WPS |
| IDS                | Yok                    | Var                   |
| Rogue AP           | Yok                    | Var                   |

---

## 3. “Bu Projeyi Neden Yaptın?” – Temel Motivasyon

Bu projeyi geliştirmemdeki temel motivasyon, mevcut ağ analiz araçlarının (ör. **Airodump-ng**, **Wireshark**) yeni başlayan veya giriş seviyesindeki kullanıcılar için fazlasıyla karmaşık ve komut satırı odaklı olmasıdır.

* **Görünürlük Problemi:** Standart cihazlar yalnızca modemleri listeler. Bu proje, ağa bağlı cihazları ve pasif trafiği görünür kılar.
* **Güvenlik Farkındalığı:** Kullanıcılar genellikle “şifre var mı?” sorusuyla yetinir. Bu proje, şifrelemenin **ne kadar güvenli olduğunu** ölçer.
* **Teknik Meydan Okuma:** Teorik ağ bilgisini, gerçek zamanlı, yüksek performanslı ve modern bir GUI ile birleştiren kapsamlı bir mühendislik ürünü ortaya koymak hedeflenmiştir.

---

## 4. Kullanılan Teknolojiler

### 4.1 Programlama Dili

* **Python 3.11+**

### 4.2 Kütüphaneler

#### Çekirdek

* Scapy
* SQLite (WAL Mode)
* Pandas
* NumPy
* manuf

#### Arayüz

* Tkinter / ttk
* Matplotlib

#### Raporlama

* ReportLab
* Jinja2
* Pillow

### 4.3 Sistem Araçları

* iw
* airmon-ng

---

## 5. Sistem Mimarisi ve Proje Yapısı

```
core/
 ├─ scanner.py
 ├─ security_analyzer.py
 ├─ ids_engine.py
 ├─ rogue_ap_detector.py
 ├─ risk_calculator.py
 └─ mac_profiler.py

gui/
 ├─ gui_main.py
 ├─ detail_panel.py
 ├─ live_graphs.py
 └─ styles.py

reports/
utils/
tests/
cli/
```

---

## 6. Temel Özellikler

### 6.1 Pasif WiFi Tarama

* Monitor mode paket yakalama
* Otomatik kanal atlama
* Beacon, Probe ve **Data frame** analizi

### 6.2 Güvenlik Analizi

* WPA2 (CCMP / TKIP) tespiti
* WPA3-SAE tespiti
* WPS durumu
* PMF (Protected Management Frames) analizi

### 6.3 Client–AP İlişkisi

* Bağlı cihazların tespiti
* Vendor ve cihaz türü analizi
* Trafik yoğunluğu ve RSSI takibi

### 6.4 IDS (Intrusion Detection System)

* Deauth flood
* Beacon flood
* Probe storm
* MAC spoofing

### 6.5 Rogue AP (Evil Twin) Tespiti

* Aynı SSID – farklı vendor
* Güvenlik protokolü uyumsuzluğu
* Şüpheli sinyal farklılıkları

---

## 7. Risk Skoru Hesaplama

Risk skoru 0–100% aralığında hesaplanır ve aşağıdaki faktörlere dayanır:

* Şifreleme türü
* Cipher suite (TKIP / CCMP)
* WPS durumu
* PMF desteği
* Evil Twin riski

**Örnek:**

* Open Network → %90–100
* WPA2-CCMP → %30
* WPA3 + PMF → %0–10

---

## 8. Kullanıcı Arayüzü (Ultra Modern GUI)

* Gradient renk paleti
* Glassmorphism efektleri
* Sağdan açılan detay paneli
* Canlı grafikler
* Risk rozetleri

Sekmeler:

* Ana Ekran
* Canlı Grafikler
* Güvenlik
* IDS Olayları
* Raporlar
* Ayarlar

---

## 9. Testler

* Scanner modülü testleri
* IDS testleri
* Güvenlik analiz testleri
* GUI ve entegrasyon testleri
* Risk skoru doğrulama testleri

---

## 10. Sonuç ve Değerlendirme

WiFi Scanner Pro, tamamen pasif analiz prensibine dayanan, etik ve yasal sınırlar içinde kalan, modern arayüzlü ve derinlemesine güvenlik analizi sunan bir sistem olarak başarıyla tamamlanmıştır.

### Gelecek Çalışmalar

* Makine öğrenmesi ile cihaz sınıflandırma
* Anomali tespiti
* Web tabanlı arayüz (FastAPI)
* Veritabanı şifreleme

---

## 11. Referanslar

* IEEE 802.11 Standard
* WiFi Security Best Practices
* Scapy Documentation
* manuf Library Documentation

---

**Geliştirici:** Musa Yoncalık
**Versiyon:** 2.0
**Durum:** ✅ Production Ready
