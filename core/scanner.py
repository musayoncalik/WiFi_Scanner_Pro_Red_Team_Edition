import logging
from scapy.all import sniff, Dot11, Dot11Beacon, Dot11ProbeReq, Dot11Elt, EAPOL, conf
import time
import threading
import subprocess
import os
from utils.helpers import db_now

log = logging.getLogger(__name__)

class WifiScanner:
    def __init__(self, db, config):
        self.db = db
        self.config = config
        
        # 1. Otomatik Arayüz Hazırlığı (Monitor Mod)
        self.iface = self._prepare_monitor_mode()
        log.info(f"Scanner Hazır: {self.iface} (5GHz & Handshake Destekli)")
        
        # --- KANAL LİSTELERİ ---
        self.ch_24ghz = list(range(1, 15)) 
        self.ch_5ghz_low = [36, 40, 44, 48, 52, 56, 60, 64] 
        self.ch_5ghz_high = [100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]
        
        # Varsayılan Kanal Listesi
        self.channels = self.ch_24ghz
        
        self.hop_paused = False
        self.hop_interval = 0.5
        self._running = False
        
        # Scapy Ayarları (Kali Linux Uyumluluğu)
        conf.sniff_promisc = True 

        # 2. MODÜLLERİ YÜKLE
        self._load_modules()

    def _prepare_monitor_mode(self):
        """Sistemi tarar, monitor modda kart arar, yoksa açar."""
        try:
            # Zaten monitor modda olan var mı?
            if os.path.exists('/sys/class/net'):
                interfaces = os.listdir('/sys/class/net')
                for iface in interfaces:
                    if iface == "lo" or iface.startswith("eth"): continue
                    try:
                        out = subprocess.check_output(['iwconfig', iface], stderr=subprocess.STDOUT).decode()
                        if "Mode:Monitor" in out: return iface
                    except: pass
            
            # Yoksa wlan0'ı zorla monitor moda al
            target_iface = "wlan0"
            log.info(f"{target_iface} monitor moda alınıyor...")
            subprocess.run(['airmon-ng', 'check', 'kill'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['airmon-ng', 'start', target_iface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2) 
            
            # Yeni ismi bul (Genelde wlan0mon olur)
            if os.path.exists('/sys/class/net'):
                interfaces = os.listdir('/sys/class/net')
                for iface in interfaces:
                    if "mon" in iface: return iface
            
            return "wlan0mon"
        except: return "wlan0"

    def _load_modules(self):
        # Profiler (OS Tahmini)
        try:
            from core.mac_profiler import MACProfiler
            self.mac_profiler = MACProfiler(self.db)
        except ImportError: 
            self.mac_profiler = None

        # Handshake Manager
        try:
            from core.handshake_manager import HandshakeManager
            self.hs_manager = HandshakeManager()
        except ImportError: 
            self.hs_manager = None

        # Güvenlik Analizörü
        try:
            from core.security_analyzer import SecurityAnalyzer
            self.security_analyzer = SecurityAnalyzer(self.db, self.config)
        except ImportError: pass

    def set_scan_mode(self, mode):
        """GUI'den gelen moda göre kanal listesini değiştirir"""
        log.info(f"Tarama Modu Değiştiriliyor: {mode}")
        
        if "Hızlı" in mode:
            self.channels = self.ch_24ghz
            self.hop_interval = 0.5
        elif "Normal" in mode:
            self.channels = self.ch_24ghz + self.ch_5ghz_low
            self.hop_interval = 0.3
        elif "Gelişmiş" in mode:
            self.channels = self.ch_5ghz_high
            self.hop_interval = 0.3
        elif "Ultra" in mode:
            self.channels = self.ch_24ghz + self.ch_5ghz_low + self.ch_5ghz_high
            self.hop_interval = 0.20
            
        if self.hop_paused: self.unlock_channel()

    def lock_channel(self, channel):
        self.hop_paused = True
        try: subprocess.run(['iw', 'dev', self.iface, 'set', 'channel', str(channel)], check=False)
        except: pass

    def unlock_channel(self): self.hop_paused = False

    def _process_packet(self, pkt):
        try:
            if not pkt.haslayer(Dot11): return

            rssi = int(pkt.dBm_AntSignal) if hasattr(pkt, 'dBm_AntSignal') and pkt.dBm_AntSignal is not None else -100
            noise = int(pkt.dBm_AntNoise) if hasattr(pkt, 'dBm_AntNoise') and pkt.dBm_AntNoise is not None else -95
            snr = rssi - noise
            
            # 1. HANDSHAKE YAKALAMA
            if self.hs_manager and pkt.haslayer(EAPOL):
                captured_bssid = self.hs_manager.check_handshake(pkt)
                if captured_bssid:
                    # Olayı veritabanına kaydet (Details sütunu artık var, hata vermez)
                    self.db.execute("INSERT INTO ids_events (ts, event_type, description, target, details) VALUES (?,?,?,?,?)",
                                    (db_now(), "HANDSHAKE", "WPA Handshake Yakalandı!", captured_bssid, "Cap file saved."))
            
            # 2. AĞ TESPİTİ (Beacon / Probe Response)
            if pkt.type == 0 and pkt.subtype in [8, 5]:
                self._process_network(pkt, rssi, noise, snr)
            
            # 3. CİHAZ (Probe Request)
            elif pkt.type == 0 and pkt.subtype == 4:
                self._process_probe_request(pkt, rssi)
            
            # 4. VERİ TRAFİĞİ (Data)
            elif pkt.type == 2:
                self._process_data_frame(pkt, rssi)
                # Ham paketi kaydet (UNIQUE hatası giderilmiş fonksiyon)
                self._store_frame(pkt, rssi)
            
            # 5. PMKID Kontrolü
            self._check_pmkid(pkt)
            
            # 6. Güvenlik Analizi
            if hasattr(self, 'security_analyzer'): self.security_analyzer.analyze_frame(pkt)

        except Exception: pass

    def _process_network(self, pkt, rssi, noise, snr):
        try:
            ssid = "<GIZLI AG>"
            channel = 0
            crypto = "Open"
            wps_enabled = False
            wifi_gen = "Wi-Fi 4"
            
            if pkt.haslayer(Dot11Elt):
                elt = pkt[Dot11Elt]
                while elt:
                    if elt.ID == 0:
                        try: ssid = elt.info.decode('utf-8', errors='ignore').strip().replace('\x00', '')
                        except: pass
                    elif elt.ID == 3: 
                        try: channel = ord(elt.info[0:1])
                        except: pass
                    elif elt.ID == 48: crypto = "WPA2"
                    elif elt.ID == 221 and b'\x00\x50\xf2\x01' in elt.info: crypto = "WPA"
                    elif elt.ID == 221 and elt.info.startswith(b'\x00\x50\xf2\x04'): wps_enabled = True
                    
                    # Wi-Fi Nesli
                    elif elt.ID == 191: wifi_gen = "Wi-Fi 5"
                    elif elt.ID == 255: wifi_gen = "Wi-Fi 6"
                    
                    elt = elt.payload.getlayer(Dot11Elt)
            
            bssid = pkt.addr3
            if not bssid: return
            
            vendor = "Bilinmiyor"
            if self.mac_profiler: vendor = self.mac_profiler.get_vendor(bssid)

            self.db.execute(
                """INSERT INTO networks (bssid, ssid, channel, crypto, generation, last_seen, vendor, rssi, noise, snr, wps_enabled)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(bssid) DO UPDATE SET
                last_seen=excluded.last_seen, rssi=excluded.rssi, noise=excluded.noise, snr=excluded.snr, generation=excluded.generation,
                ssid=CASE WHEN ssid = '<GIZLI AG>' THEN excluded.ssid ELSE ssid END
                """, (bssid, ssid, channel, crypto, wifi_gen, db_now(), vendor, rssi, noise, snr, wps_enabled)
            )
        except Exception: pass

    def _process_probe_request(self, pkt, rssi):
        try:
            client = pkt.addr2
            if not client: return
            
            vendor = "Bilinmiyor"
            os_guess = "Bilinmiyor"
            
            if self.mac_profiler:
                vendor = self.mac_profiler.get_vendor(client)
                os_guess = self.mac_profiler.profile_device(pkt, vendor)
            
            self.db.execute("INSERT OR REPLACE INTO clients (mac, last_seen, rssi, vendor, device_type, os_guess) VALUES (?,?,?,?,?,?)",
                            (client, db_now(), rssi, vendor, "Mobile", os_guess))
        except: pass

    def _process_data_frame(self, pkt, rssi):
        try:
            if not hasattr(pkt, 'FCfield'): return
            to_ds, from_ds = pkt.FCfield & 0x01, pkt.FCfield & 0x02
            client, ap = None, None
            
            if to_ds and not from_ds: client, ap = pkt.addr2, pkt.addr1
            elif from_ds and not to_ds: client, ap = pkt.addr1, pkt.addr2
            
            if client and ap and client != "ff:ff:ff:ff:ff:ff":
                vendor = "Bilinmiyor"
                if self.mac_profiler: vendor = self.mac_profiler.get_vendor(client)
                
                self.db.execute("INSERT OR REPLACE INTO clients (mac, last_seen, rssi, vendor, device_type, bssid_connected) VALUES (?,?,?,?,?,?)",
                                (client, db_now(), rssi, vendor, "Station", ap))
                self.db.execute("INSERT INTO client_connections (client_mac, ap_bssid, last_seen, rssi) VALUES (?, ?, ?, ?) ON CONFLICT DO UPDATE SET last_seen=excluded.last_seen, rssi=excluded.rssi",
                                (client, ap, db_now(), rssi))
        except: pass

    def _check_pmkid(self, pkt):
        try:
            if pkt.haslayer(EAPOL):
                eapol = pkt[EAPOL]
                if hasattr(eapol, 'key_data') and eapol.key_data:
                    kd = bytes(eapol.key_data)
                    if len(kd) >= 16:
                        pmkid = kd[:16].hex()
                        bssid = getattr(pkt, 'addr3', 'unknown')
                        self.db.execute("INSERT INTO recommendations (ts, target, recommendation) VALUES (?,?,?)",
                                        (db_now(), bssid, f"PMKID Yakalandı: {pmkid}"))
        except: pass

    def _store_frame(self, pkt, rssi):
        # KRİTİK DÜZELTME: INSERT OR IGNORE kullanarak UNIQUE hatasını önlüyoruz
        try: 
            self.db.execute("INSERT OR IGNORE INTO frames (ts, type, subtype, src, dst, bssid, rssi, raw) VALUES (?,?,?,?,?,?,?,?)", 
                            (db_now(), str(pkt.type), str(pkt.subtype), pkt.addr2, pkt.addr1, pkt.addr3, rssi, bytes(pkt)))
        except: pass

    def _scapy_sniff(self, stop_event):
        log.info("Paket dinleme başladı...")
        while not stop_event.is_set():
            try: sniff(iface=self.iface, prn=self._process_packet, timeout=1, store=0, monitor=True)
            except: time.sleep(1)

    def _channel_hopper(self, stop_event):
        idx = 0
        while not stop_event.is_set():
            if self.hop_paused: 
                time.sleep(1)
                continue
            
            if not self.channels: self.channels = list(range(1,14))
            
            ch = self.channels[idx % len(self.channels)]
            try: subprocess.run(['iw', 'dev', self.iface, 'set', 'channel', str(ch)], check=False)
            except: pass
            
            time.sleep(self.hop_interval)
            idx += 1

    def run(self, stop_event):
        self._running = True
        log.info("Scanner threadleri başlatılıyor...")
        t1 = threading.Thread(target=self._scapy_sniff, args=(stop_event,), daemon=True)
        t1.start()
        t2 = threading.Thread(target=self._channel_hopper, args=(stop_event,), daemon=True)
        t2.start()
        while not stop_event.is_set(): time.sleep(0.5)
        self._running = False