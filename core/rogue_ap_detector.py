import threading
import time
import logging

log = logging.getLogger(__name__)

class RogueAPDetector:
    def __init__(self, db, config):
        self.db = db
        self.config = config
        self.whitelist = []  # İleride güvenilir ağlar eklenebilir
        self._stop_event = None
        # Varsayılan ayar: Bir SSID için en fazla kaç BSSID normal kabul edilir?
        self.max_bssids = 2 

    def is_evil_twin(self, network):
        """
        Bir ağın Evil Twin (Şeytani İkiz) olup olmadığını kontrol eder.
        True dönerse o ağ yüksek risklidir.
        """
        try:
            ssid = network.get('ssid')
            bssid = network.get('bssid')
            
            # Gizli ağlar veya ismi olmayanlar için kontrol yapılamaz
            if not ssid or ssid == "<GIZLI AG>": 
                return False

            # Veritabanında AYNI İSME (SSID) sahip ama FARKLI ADRESE (BSSID) sahip ağları bul
            duplicates = self.db.query("SELECT * FROM networks WHERE ssid = ? AND bssid != ?", (ssid, bssid))
            
            if duplicates:
                for dup in duplicates:
                    # KRİTER 1: Şifreleme Farklılığı (En Güçlü Belirti)
                    # Örnek: Orijinal ağ WPA2 iken, sahte ağ Open (Şifresiz) yayın yapar.
                    current_crypto = str(network.get('crypto', '')).upper()
                    dup_crypto = str(dup['crypto']).upper()
                    
                    if "OPEN" in current_crypto and "WPA" in dup_crypto:
                        return True # Sahte ağ (Open) tespit edildi!
                    
                    if "WPA" in current_crypto and "OPEN" in dup_crypto:
                        return True # Orijinal ağ tespit edildi (ama ortamda sahtesi var)

                    # KRİTER 2: Kanal Farklılığı (Opsiyonel)
                    # Kurumsal ağlarda (Mesh) farklı kanallar normaldir, o yüzden tek başına yeterli değil.
                    # Ancak ev ağlarında aynı isimde farklı kanal şüphelidir.
                
                # Eğer 2'den fazla kopya varsa ve şifreleme aynıysa bile şüphelidir (DDoS / Flood)
                if len(duplicates) >= self.max_bssids:
                    return True
                
                # Sadece 1 kopya varsa ve şifreleme aynıysa Mesh sistemi olabilir, False dön.
                return False
                
        except Exception as e:
            log.error(f"Evil Twin kontrol hatası: {e}")
        return False

    def check_and_alert(self):
        """
        Tüm veritabanını tarar ve tespit edilen Rogue AP'leri liste olarak döndürür.
        """
        rogues = []
        try:
            # Sadece ismi olan ağları çek
            networks = self.db.query("SELECT * FROM networks WHERE ssid != '<GIZLI AG>'")
            
            for net in networks:
                net_dict = dict(net)
                if self.is_evil_twin(net_dict):
                    # Riskli ağ bulundu!
                    rogues.append({
                        "ssid": net_dict['ssid'],
                        "bssid": net_dict['bssid'],
                        "type": "Evil Twin / Rogue AP",
                        "risk_score": 1.0 # %100 Risk
                    })
                    
                    # Olayı veritabanına logla (Eğer daha önce loglanmadıysa)
                    self._log_rogue_event(net_dict)

        except Exception as e:
            log.error(f"Genel Rogue tarama hatası: {e}")
        
        return rogues

    def _log_rogue_event(self, net):
        """Tespit edilen Rogue AP'yi IDS olaylarına kaydeder"""
        try:
            # Son 1 dakikada aynı olay kaydedildi mi?
            last = self.db.query(
                "SELECT ts FROM ids_events WHERE event_type='ROGUE_AP' AND target=? ORDER BY ts DESC LIMIT 1", 
                (net['bssid'],)
            )
            
            import time
            if last and (time.time() - last[0]['ts'] < 60):
                return # Tekrar kaydetme

            self.db.execute(
                "INSERT INTO ids_events (ts, event_type, description, target, data) VALUES (?, ?, ?, ?, ?)",
                (time.time(), "ROGUE_AP", f"Evil Twin Tespiti: {net['ssid']}", net['bssid'], "High Risk")
            )
            log.warning(f"Rogue AP Tespit Edildi: {net['ssid']} ({net['bssid']})")
            
        except Exception: pass

    def run(self, stop_event):
        """
        Arka planda çalışan Thread döngüsü.
        Main.py tarafından başlatılır.
        """
        self._stop_event = stop_event
        log.info("Rogue AP Detector servisi başlatıldı.")
        
        while not stop_event.is_set():
            try:
                # Taramayı gerçekleştir
                self.check_and_alert()
            except Exception as e:
                log.error(f"Rogue Thread Hatası: {e}")
            
            # 10 saniye bekle (Donmayı önleyen wait mekanizması)
            # Eğer stop_event gelirse 10 saniyeyi beklemeden hemen çıkar.
            if stop_event.wait(timeout=10):
                break
        
        log.info("Rogue AP Detector servisi durduruldu.")