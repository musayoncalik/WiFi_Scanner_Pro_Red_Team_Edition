import logging
import time
import threading
from utils.helpers import db_now

log = logging.getLogger(__name__)

class IDSEngine:
    def __init__(self, db, config, event_bus=None):
        self.db = db
        self.config = config
        self.event_bus = event_bus # İleride bildirim sistemi için
        
        # Tarama aralığı (saniye)
        self.poll_interval = config.getint('ids', 'poll_interval', fallback=2)
        
        # Analiz penceresi (son X saniyedeki paketlere bak)
        self.window_seconds = config.getint('ids', 'window_seconds', fallback=10)
        
        # Uyarı Bastırma (Alert Suppression) için hafıza
        # Aynı uyarıyı tekrar tekrar loglamamak için kullanılır.
        self._suppress_cache = {} 
        self._stop_event = None

    def _should_alert(self, event_key, timeout=60):
        """
        Belirli bir olayın (event_key) son 'timeout' saniye içinde 
        zaten raporlanıp raporlanmadığını kontrol eder.
        True dönerse raporla, False dönerse sessiz kal.
        """
        now = time.time()
        if event_key in self._suppress_cache:
            last_time = self._suppress_cache[event_key]
            if now - last_time < timeout:
                return False # Henüz zaman aşımı dolmadı, sessiz kal
        
        # Yeni zamanı kaydet ve onayı ver
        self._suppress_cache[event_key] = now
        
        # Cache temizliği (Hafıza şişmesini önle)
        if len(self._suppress_cache) > 500:
            self._suppress_cache = {k:v for k,v in self._suppress_cache.items() if now - v < 300}
            
        return True

    def _log_event(self, event_type, desc, data_str, target="Genel"):
        """Veritabanına güvenli şekilde olay kaydeder"""
        try:
            self.db.execute(
                "INSERT INTO ids_events (ts, event_type, description, data, target) VALUES (?,?,?,?,?)",
                (db_now(), event_type, desc, data_str, target)
            )
            log.warning(f"IDS UYARISI: {event_type} -> {desc}")
        except Exception as e:
            log.error(f"IDS Loglama Hatası: {e}")

    def check_deauth_flood(self):
        """Deauthentication saldırılarını (Ağdan düşürme) tespit eder"""
        try:
            window_start = db_now() - self.window_seconds
            # Type 0 (Yönetim), Subtype 12 (Deauth)
            rows = self.db.query(
                "SELECT COUNT(*) as c FROM frames WHERE type='0' AND subtype='12' AND ts > ?",
                (window_start,)
            )
            count = rows[0]['c'] if rows else 0
            threshold = self.config.getint('ids', 'deauth_threshold', fallback=30) # Eşik değeri
            
            if count > threshold:
                if self._should_alert('deauth_flood', timeout=30):
                    self._log_event(
                        'DEAUTH_FLOOD', 
                        f"Aşırı Deauth Paketi: {count} adet / {self.window_seconds}sn", 
                        f"Count: {count}, Threshold: {threshold}",
                        target="Broadcast"
                    )
        except Exception: pass

    def check_probe_storm(self):
        """Probe Request fırtınasını (Aşırı tarama) tespit eder"""
        try:
            window_start = db_now() - self.window_seconds
            # Type 0, Subtype 4 (Probe Request)
            rows = self.db.query(
                "SELECT COUNT(*) as c FROM frames WHERE type='0' AND subtype='4' AND ts > ?",
                (window_start,)
            )
            count = rows[0]['c'] if rows else 0
            threshold = self.config.getint('ids', 'probe_threshold', fallback=150)
            
            if count > threshold:
                if self._should_alert('probe_storm', timeout=60):
                    self._log_event(
                        'PROBE_STORM',
                        f"Probe Request Fırtınası: {count} adet",
                        f"Count: {count}, Threshold: {threshold}"
                    )
        except Exception: pass

    def check_beacon_flood(self):
        """Sahte ağ (Beacon) yayını saldırılarını tespit eder"""
        try:
            window_start = db_now() - self.window_seconds
            # Type 0, Subtype 8 (Beacon)
            rows = self.db.query(
                "SELECT COUNT(*) as c FROM frames WHERE type='0' AND subtype='8' AND ts > ?",
                (window_start,)
            )
            count = rows[0]['c'] if rows else 0
            threshold = self.config.getint('ids', 'beacon_threshold', fallback=200)
            
            if count > threshold:
                if self._should_alert('beacon_flood', timeout=60):
                    self._log_event(
                        'BEACON_FLOOD',
                        f"Beacon Flood Tespiti: {count} adet",
                        f"Count: {count}, Threshold: {threshold}"
                    )
        except Exception: pass

    def check_association_flood(self):
        """Association Flood (Bağlantı isteği boğma) saldırısını tespit eder"""
        try:
            window_start = db_now() - self.window_seconds
            # Type 0, Subtype 0 (Association Req)
            rows = self.db.query(
                "SELECT COUNT(*) as c FROM frames WHERE type='0' AND subtype='0' AND ts > ?",
                (window_start,)
            )
            count = rows[0]['c'] if rows else 0
            threshold = self.config.getint('ids', 'assoc_threshold', fallback=50)
            
            if count > threshold:
                if self._should_alert('assoc_flood', timeout=60):
                    self._log_event(
                        'ASSOC_FLOOD',
                        f"Association Flood: {count} istek",
                        f"Count: {count}, Threshold: {threshold}"
                    )
        except Exception: pass

    def check_mac_spoofing(self):
        """Aynı MAC adresinin çok kısa sürede farklı AP'lere bağlanmaya çalışmasını izler"""
        try:
            window_start = db_now() - self.window_seconds
            # Bir kaynak (src), kaç farklı hedefe (bssid) paket göndermiş?
            rows = self.db.query(
                """
                SELECT src, COUNT(DISTINCT bssid) as target_count
                FROM frames
                WHERE ts > ? AND src IS NOT NULL AND type='2' -- Sadece veri paketleri
                GROUP BY src
                HAVING target_count > 5
                """,
                (window_start,)
            )
            
            for row in rows:
                mac = row['src']
                count = row['target_count']
                
                # Rastgele MAC kullanan cihazları elemek için basit kontrol (Locally Administered Bit)
                # Burası opsiyoneldir, şimdilik kapatıyorum.
                
                if self._should_alert(f'spoofing_{mac}', timeout=120):
                    self._log_event(
                        'MAC_SPOOFING',
                        f"Şüpheli MAC Hareketi: {mac} -> {count} farklı hedef",
                        f"MAC: {mac}, Targets: {count}",
                        target=mac
                    )
        except Exception: pass

    def run(self, stop_event):
        """Thread Döngüsü"""
        self._stop_event = stop_event
        log.info("IDS Motoru (Saldırı Tespit Sistemi) başlatıldı.")
        
        while not stop_event.is_set():
            try:
                # Saldırı Kontrolleri
                self.check_deauth_flood()
                self.check_probe_storm()
                self.check_beacon_flood()
                self.check_association_flood()
                self.check_mac_spoofing()
                
            except Exception as e:
                log.error(f"IDS Analiz Hatası: {e}")
            
            # Donmayı önleyen akıllı bekleme
            if stop_event.wait(timeout=self.poll_interval):
                break
        
        log.info("IDS Motoru durduruldu.")