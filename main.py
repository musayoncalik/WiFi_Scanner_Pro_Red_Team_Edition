#!/usr/bin/env python3
import logging
import sys
import time
import threading
import os

# Modüller
from utils.db import Database
from core.scanner import WifiScanner
from core.ids_engine import IDSEngine
from core.rogue_ap_detector import RogueAPDetector
from gui.gui_main import WifiGuiApp

# Basit Konfigürasyon Sınıfı
class Config:
    def get(self, section, key, fallback=None): return fallback
    def getint(self, section, key, fallback=0): return int(fallback)

# Logger Ayarı
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("WiFiScanner")

def main():
    log.info("="*60)
    log.info("WiFi Scanner Projesi Başlatılıyor (v2.0)")
    log.info("="*60)

    # 1. Temel Bileşenleri Başlat
    config = Config()
    
    # Veritabanı (Tablolar yoksa utils/db.py otomatik oluşturur)
    try:
        db = Database()
    except Exception as e:
        log.critical(f"Veritabanı başlatılamadı: {e}")
        return

    # Thread Durdurma Sinyali (Tüm işçiler bunu dinler)
    stop_event = threading.Event()

    # 2. Modülleri Oluştur
    log.info("Analiz modülleri yükleniyor...")
    scanner = WifiScanner(db, config)
    ids = IDSEngine(db, config)
    rogue = RogueAPDetector(db, config)

    # 3. Arka Plan İşçilerini (Threads) Başlat
    threads = []

    # A) Scanner Thread (Paket Yakalama)
    t_scanner = threading.Thread(target=scanner.run, args=(stop_event,), name="Scanner", daemon=True)
    t_scanner.start()
    threads.append(t_scanner)
    log.info("-> Scanner servisi aktif.")

    # B) IDS Thread (Saldırı Tespiti)
    t_ids = threading.Thread(target=ids.run, args=(stop_event,), name="IDS", daemon=True)
    t_ids.start()
    threads.append(t_ids)
    log.info("-> IDS servisi aktif.")

    # C) Rogue Detector Thread (Sahte AP Tespiti)
    # NOT: Artık sınıfın içindeki 'run' metodunu kullanıyoruz.
    t_rogue = threading.Thread(target=rogue.run, args=(stop_event,), name="RogueDetector", daemon=True)
    t_rogue.start()
    threads.append(t_rogue)
    log.info("-> Rogue AP dedektörü aktif.")

    # 4. GUI Başlatma (Ana Thread)
    log.info("Grafik Arayüz (GUI) hazırlanıyor...")
    
    try:
        # GUI, ana thread'i bloke eder (pencere kapanana kadar burası çalışır)
        app = WifiGuiApp(db, scanner, ids, config)
        app.run() 
    except KeyboardInterrupt:
        log.info("Kullanıcı tarafından durduruldu (CTRL+C).")
    except Exception as e:
        log.critical(f"Kritik Hata: {e}", exc_info=True)
    finally:
        # 5. Temiz Kapanış (Graceful Shutdown)
        log.info("Kapatılıyor... Lütfen bekleyin.")
        
        # Tüm thread'lere dur emri ver
        stop_event.set()
        
        # Scanner kanal kilidini aç (Sistem normal dönsün)
        if hasattr(scanner, 'unlock_channel'):
            scanner.unlock_channel()

        # Thread'lerin bitmesini bekle (Timeout: 2 saniye)
        for t in threads:
            t.join(timeout=2.0)
            if t.is_alive():
                log.warning(f"Thread kapatılamadı (Zaman aşımı): {t.name}")
            else:
                log.info(f"Servis durduruldu: {t.name}")

        db.close()
        log.info("Program başarıyla sonlandırıldı.")

if __name__ == "__main__":
    # Root Kontrolü
    if os.geteuid() != 0:
        log.error("Bu yazılım Monitor Mode kullanmak için ROOT yetkisi gerektirir.")
        log.error("Lütfen 'sudo -E python3 main.py' komutu ile çalıştırın.")
        sys.exit(1)

    # X11 İzinleri (Kali Linux GUI Sorunları İçin)
    os.system("xhost +local:root > /dev/null 2>&1")
    
    main()