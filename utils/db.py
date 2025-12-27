import sqlite3
import logging
import os
import time

log = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path="data/wifi_scanner.db"):
        self.db_path = db_path
        # Klasör yoksa oluştur
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Veritabanı tablolarını ve performans ayarlarını başlatır"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # --- KRİTİK PERFORMANS AYARLARI ---
            # WAL Modu: Okuma ve yazma işlemlerinin aynı anda yapılmasına izin verir (Donmayı önler).
            c.execute('PRAGMA journal_mode=WAL;') 
            c.execute('PRAGMA synchronous=NORMAL;')
            c.execute('PRAGMA cache_size=10000;')
            
            # 1. AĞLAR TABLOSU (Networks)
            c.execute('''CREATE TABLE IF NOT EXISTS networks (
                            bssid TEXT PRIMARY KEY, 
                            ssid TEXT, 
                            channel INTEGER, 
                            crypto TEXT, 
                            generation TEXT DEFAULT 'Wi-Fi 4', 
                            last_seen REAL, 
                            first_seen REAL,
                            vendor TEXT, 
                            rssi INTEGER,
                            noise INTEGER DEFAULT -95,
                            snr INTEGER DEFAULT 0,
                            channel_width INTEGER DEFAULT 20,
                            phy_type TEXT DEFAULT '802.11n',
                            wps_enabled BOOLEAN DEFAULT 0,
                            hidden BOOLEAN DEFAULT 0
                        )''')
            
            # 2. CİHAZLAR TABLOSU (Clients)
            c.execute('''CREATE TABLE IF NOT EXISTS clients (
                            mac TEXT PRIMARY KEY, 
                            last_seen REAL, 
                            first_seen REAL,
                            rssi INTEGER, 
                            vendor TEXT, 
                            device_type TEXT,
                            os_guess TEXT,          
                            bssid_connected TEXT
                        )''')
            
            # 3. IOT/BLE CİHAZLARI TABLOSU
            c.execute('''CREATE TABLE IF NOT EXISTS iot_devices (
                            mac TEXT PRIMARY KEY,
                            name TEXT,
                            rssi INTEGER,
                            device_type TEXT, 
                            vendor TEXT,
                            last_seen REAL
                        )''')
            
            # 4. BAĞLANTILAR TABLOSU (Connections)
            c.execute('''CREATE TABLE IF NOT EXISTS client_connections (
                            client_mac TEXT, 
                            ap_bssid TEXT, 
                            last_seen REAL, 
                            rssi INTEGER, 
                            frame_count INTEGER DEFAULT 1, 
                            PRIMARY KEY (client_mac, ap_bssid)
                        )''')
            
            # 5. HAM PAKETLER (Frames)
            c.execute('''CREATE TABLE IF NOT EXISTS frames (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ts REAL, 
                            type TEXT, 
                            subtype TEXT, 
                            src TEXT, 
                            dst TEXT, 
                            bssid TEXT, 
                            rssi INTEGER, 
                            raw BLOB,
                            UNIQUE(src, dst, type, subtype, ts)
                        )''')
            
            # 6. IDS OLAYLARI (Güvenlik) - DÜZELTME: 'details' EKLENDİ
            # AutoPilot buraya 'details' sütunu üzerinden yazıyor.
            c.execute('''CREATE TABLE IF NOT EXISTS ids_events (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            ts REAL, 
                            event_type TEXT, 
                            target TEXT,
                            details TEXT, 
                            description TEXT, 
                            data TEXT
                        )''')
            
            # 7. ÖNERİLER (Recommendations)
            c.execute('''CREATE TABLE IF NOT EXISTS recommendations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            ts REAL, 
                            target TEXT, 
                            recommendation TEXT
                        )''')

            conn.commit()
            conn.close()
            log.info(f"Veritabanı hazır (WAL Modu): {self.db_path}")
            
        except Exception as e:
            log.error(f"DB Başlatma Hatası: {e}")

    # Main.py uyumluluğu için
    def migrate(self): pass

    def execute(self, query, params=()):
        """Veri yazma işlemleri için güvenli fonksiyon"""
        try:
            # timeout=10: Database Locked hatasını önler
            conn = sqlite3.connect(self.db_path, timeout=10, check_same_thread=False)
            c = conn.cursor()
            c.execute(query, params)
            conn.commit()
            conn.close()
        except Exception as e:
            log.error(f"DB Yazma Hatası: {e} | Sorgu: {query}")

    def query(self, query, params=()):
        """Veri okuma işlemleri için güvenli fonksiyon"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=10, check_same_thread=False)
            conn.row_factory = sqlite3.Row # Sonuçları sözlük (dict) gibi almayı sağlar
            c = conn.cursor()
            c.execute(query, params)
            rows = c.fetchall()
            conn.close()
            return rows
        except Exception as e:
            log.error(f"DB Okuma Hatası: {e}")
            return []

    def close(self): pass