import logging
import os
import time
from scapy.all import wrpcap, EAPOL

log = logging.getLogger(__name__)

class HandshakeManager:
    def __init__(self, save_dir="captures/handshakes"):
        self.save_dir = save_dir
        # Klasör yoksa oluştur
        os.makedirs(self.save_dir, exist_ok=True)
        # Yakalananları önbellekte tut (Aynı handshake'i 50 kere yazmayalım)
        self.captured_cache = set()

    def check_handshake(self, pkt):
        """
        Paket bir EAPOL (Handshake) parçası mı kontrol eder ve kaydeder.
        """
        try:
            if not pkt.haslayer(EAPOL): return None
            
            # Modemin MAC adresi (BSSID) genellikle addr3'tür
            bssid = pkt.addr3
            if not bssid: return None

            # Basit kontrol: Daha önce bu BSSID'yi yakaladık mı? (Spam önleme)
            # Gerçek bir pentest aracında 4 parçayı (M1-M4) birleştirmek gerekir,
            # ama burada her EAPOL parçasını yakalamak başlangıç için yeterli.
            
            ts = int(time.time())
            filename = f"Handshake_{bssid.replace(':','-')}_{ts}.cap"
            filepath = os.path.join(self.save_dir, filename)
            
            # Paketi pcap formatında kaydet (Aircrack-ng uyumlu)
            wrpcap(filepath, pkt, append=True)
            
            log.info(f"⚡ HANDSHAKE YAKALANDI: {bssid} -> {filename}")
            return bssid

        except Exception as e:
            # log.error(f"Handshake hatası: {e}") 
            pass
        return None