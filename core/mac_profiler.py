import logging
import sqlite3
import os

# Scapy importunu fonksiyon içine alacağız (Performans için)

log = logging.getLogger(__name__)

try:
    from manuf import manuf
    MANUF_AVAILABLE = True
except ImportError:
    MANUF_AVAILABLE = False
    log.warning("manuf kütüphanesi bulunamadı, OUI veritabanı/fallback kullanılacak")

class MACProfiler:
    
    def __init__(self, db, oui_db_path='data/oui_database.db'):
        self.db = db
        self.oui_db_path = oui_db_path
        self.oui_cache = {}
        
        # Manuf Yükleme
        if MANUF_AVAILABLE:
            try:
                self.manuf_parser = manuf.MacParser(update=False)
                log.info("MAC Profiler: manuf kütüphanesi aktif.")
            except Exception:
                self.manuf_parser = None
        else:
            self.manuf_parser = None
            if os.path.exists(oui_db_path):
                self._load_oui_db()

    def _load_oui_db(self):
        """Yerel OUI veritabanı varsa yükle (Yedek plan)"""
        try:
            conn = sqlite3.connect(self.oui_db_path)
            cur = conn.cursor()
            cur.execute("SELECT prefix, vendor FROM oui")
            for prefix, vendor in cur.fetchall():
                self.oui_cache[prefix.upper()] = vendor
            conn.close()
        except Exception: pass

    def get_vendor(self, mac):
        """MAC adresinden üreticiyi bulur (Scanner tarafından kullanılır)"""
        if not mac: return "Bilinmiyor"
        
        # 1. Manuf Kütüphanesi
        if self.manuf_parser:
            try:
                vendor = self.manuf_parser.get_manuf(mac)
                if vendor and vendor != "Unknown": return vendor
            except: pass
        
        # 2. Yerel OUI Cache
        clean_mac = mac.upper().replace(":", "").replace("-", "")[:6]
        if clean_mac in self.oui_cache:
            return self.oui_cache[clean_mac]
            
        return "Bilinmiyor"

    def detect_device_type(self, vendor):
        """Üretici isminden cihaz türünü (Mobile, PC, Router) tahmin eder"""
        if not vendor: return "Diğer"
        v = vendor.lower()
        
        if any(x in v for x in ['apple', 'samsung', 'huawei', 'xiaomi', 'oppo', 'vivo', 'google', 'lg', 'oneplus']):
            return "Mobile"
        if any(x in v for x in ['intel', 'dell', 'hp', 'lenovo', 'asus', 'msi', 'microsoft']):
            return "PC/Laptop"
        if any(x in v for x in ['tp-link', 'zyxel', 'netgear', 'd-link', 'cisco', 'ubiquiti', 'tenda']):
            return "Router/AP"
        if any(x in v for x in ['espressif', 'tuya', 'nest', 'amazon']):
            return "IoT"
            
        return "Diğer"

    def profile_device(self, pkt, vendor):
        """
        GELİŞMİŞ ANALİZ:
        Paketin 'Capabilities' (Yetenek) alanlarını okuyarak OS tahmini yapar.
        Bu fonksiyon Scanner tarafından çağrılır.
        """
        os_guess = "Bilinmiyor"
        caps = []

        # Paket içeriğini analiz et
        try:
            from scapy.all import Dot11Elt
            if pkt.haslayer(Dot11Elt):
                elt = pkt[Dot11Elt]
                while elt:
                    # ID 45: HT Capabilities (802.11n - Wi-Fi 4)
                    if elt.ID == 45: 
                        caps.append("HT")
                    
                    # ID 191: VHT Capabilities (802.11ac - Wi-Fi 5)
                    elif elt.ID == 191: 
                        caps.append("VHT")
                    
                    # ID 255: HE Capabilities (802.11ax - Wi-Fi 6)
                    elif elt.ID == 255: 
                        caps.append("HE")
                        # Gelecekte EHT (Wi-Fi 7) buraya eklenebilir
                        
                    elt = elt.payload.getlayer(Dot11Elt)
        except: pass

        # --- HEURISTIC (ZEKA) MOTORU ---
        # Üretici + Wi-Fi Yeteneği = OS Tahmini
        
        vendor_lower = str(vendor).lower()

        # 1. APPLE CİHAZLARI
        if "apple" in vendor_lower:
            if "HE" in caps:
                os_guess = "iOS 15+ / macOS (Wi-Fi 6)"
            elif "VHT" in caps:
                os_guess = "iOS 10-14 (Wi-Fi 5)"
            elif "HT" in caps:
                os_guess = "Eski iOS (iPhone 4s-5)"
            else:
                os_guess = "Apple (Legacy)"

        # 2. ANDROID CİHAZLARI (Samsung, Google, vb.)
        elif any(x in vendor_lower for x in ["samsung", "google", "huawei", "xiaomi", "oppo"]):
            if "HE" in caps:
                os_guess = "Android 11+ (Wi-Fi 6)"
            elif "VHT" in caps:
                os_guess = "Android 8-10"
            else:
                os_guess = "Android (Eski)"

        # 3. WINDOWS / PC
        elif any(x in vendor_lower for x in ["intel", "microsoft", "dell", "hp", "lenovo"]):
            if "HE" in caps:
                os_guess = "Windows 11 / Modern Linux"
            else:
                os_guess = "Windows 10 / Linux"
                
        # 4. IoT CİHAZLARI
        elif any(x in vendor_lower for x in ["espressif", "tuya"]):
            os_guess = "RTOS (IoT)"

        return os_guess