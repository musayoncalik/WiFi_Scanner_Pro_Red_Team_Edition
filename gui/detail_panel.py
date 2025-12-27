import tkinter as tk
from tkinter import ttk
import time
from gui.styles import COLORS, FONTS
from gui.live_graphs import RSSIGraph

class DetailPanel:
    def __init__(self, parent, db, risk_calc, rogue_detect, snr_analyzer, channel_analyzer, scanner=None):
        self.parent = parent
        self.db = db
        self.risk_calc = risk_calc
        self.rogue_detect = rogue_detect
        self.snr_analyzer = snr_analyzer
        self.channel_analyzer = channel_analyzer
        self.scanner = scanner
        
        self.current_bssid = None
        self.panel = tk.Frame(parent, bg=COLORS['bg_primary'])
        
        self._build_ui()

    def _build_ui(self):
        # --- ÜST BAŞLIK (Header) ---
        self.header_frame = tk.Frame(self.panel, bg=COLORS['primary'], height=70)
        self.header_frame.pack(fill='x')
        self.header_frame.pack_propagate(False) # Boyutu sabitle
        
        # Kapat Butonu
        btn_close = tk.Button(self.header_frame, text="✕", font=('Arial', 12, 'bold'), 
                              bg=COLORS['primary'], fg='white', bd=0, 
                              activebackground=COLORS['danger'], command=self.hide)
        btn_close.pack(side='right', anchor='n', padx=10, pady=10)
        
        # SSID ve BSSID Etiketleri
        self.lbl_ssid = tk.Label(self.header_frame, text="Ağ Seçilmedi", font=('Inter', 14, 'bold'), bg=COLORS['primary'], fg='white')
        self.lbl_ssid.pack(side='top', pady=(10, 2))
        self.lbl_bssid = tk.Label(self.header_frame, text="--:--:--:--:--:--", font=('Consolas', 10), bg=COLORS['primary'], fg='#dddddd')
        self.lbl_bssid.pack(side='top')

        # --- SEKMELER (Notebook) ---
        self.notebook = ttk.Notebook(self.panel)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        self._init_tabs()

    def _init_tabs(self):
        # 1. Genel Bilgi Sekmesi
        self.tab_general = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_general, text="ℹ️ Genel")
        self.txt_general = tk.Text(self.tab_general, bg="#1e1e1e", fg="white", font=("Consolas", 10), padx=10, pady=10, bd=0)
        self.txt_general.pack(fill='both', expand=True)

        # 2. RF & Sinyal Sekmesi
        self.tab_rf = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_rf, text="📡 RF & Sinyal")
        self.txt_rf = tk.Text(self.tab_rf, bg="#1e1e1e", fg="#00ffcc", font=("Consolas", 10), padx=10, pady=10, bd=0)
        self.txt_rf.pack(fill='both', expand=True)

        # 3. Güvenlik Sekmesi
        self.tab_sec = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sec, text="🛡️ Güvenlik")
        self.txt_sec = tk.Text(self.tab_sec, bg="#1e1e1e", fg="#ff5555", font=("Consolas", 10), padx=10, pady=10, bd=0)
        self.txt_sec.pack(fill='both', expand=True)

        # 4. Cihazlar (Clients) Sekmesi
        self.tab_clients = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_clients, text="👥 Cihazlar")
        
        # Treeview (Tablo) yapısı
        cols = ("mac", "vendor", "type", "rssi")
        self.client_tree = ttk.Treeview(self.tab_clients, columns=cols, show='headings', height=10)
        
        self.client_tree.heading("mac", text="MAC Adresi")
        self.client_tree.column("mac", width=120)
        
        self.client_tree.heading("vendor", text="Üretici")
        self.client_tree.column("vendor", width=150)
        
        self.client_tree.heading("type", text="Cihaz Türü")
        self.client_tree.column("type", width=100)
        
        self.client_tree.heading("rssi", text="Sinyal")
        self.client_tree.column("rssi", width=80)
        
        self.client_tree.pack(fill='both', expand=True)

        # 5. Canlı Grafik (Mini)
        self.tab_graph = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_graph, text="📈 Canlı")
        self.mini_rssi = RSSIGraph(self.tab_graph, max_points=50)
        self.mini_rssi.frame.pack(fill='both', expand=True, padx=5, pady=5)

    def show(self, bssid):
        self.current_bssid = bssid
        # Paneli Parent (PanedWindow)'a ekle
        try: self.parent.add(self.panel, weight=1)
        except: pass 
        self.refresh()

    def hide(self):
        self.current_bssid = None
        try: self.parent.forget(self.panel)
        except: pass

    def refresh(self):
        if not self.current_bssid: return
        
        # Veritabanından en güncel veriyi çek
        rows = self.db.query("SELECT * FROM networks WHERE bssid=?", (self.current_bssid,))
        if not rows: return
        net = dict(rows[0])
        
        # Başlık ve Renk Güncelleme (Risk durumuna göre)
        risk_score = self.risk_calc.calculate_network_risk(net)
        header_color = self.risk_calc.get_risk_color(risk_score)
        
        self.header_frame.configure(bg=header_color)
        self.lbl_ssid.configure(bg=header_color, text=net.get('ssid') or "Gizli Ağ")
        self.lbl_bssid.configure(bg=header_color, text=net.get('bssid'))
        
        # --- 1. SEKME: GENEL BİLGİ ---
        first_seen = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(net.get('first_seen', 0))) if net.get('first_seen') else "Bilinmiyor"
        last_seen = time.strftime('%H:%M:%S', time.localtime(net.get('last_seen', 0)))
        
        info_text = f"""
 [AĞ KİMLİĞİ]
 ====================================
 SSID          : {net.get('ssid')}
 BSSID         : {net.get('bssid')}
 Üretici       : {net.get('vendor', 'Bilinmiyor')}
 Gizli Ağ      : {'EVET' if net.get('ssid') == '<GIZLI AG>' else 'HAYIR'}
 
 [ZAMAN BİLGİSİ]
 ====================================
 İlk Görülme   : {first_seen}
 Son Görülme   : {last_seen}
        """
        self.txt_general.delete('1.0', 'end')
        self.txt_general.insert('end', info_text)

        # --- 2. SEKME: RF & SİNYAL ---
        rssi = net.get('rssi', -100)
        noise = net.get('noise', -95)
        snr = net.get('snr', 0)
        channel = net.get('channel', 0)
        
        # SNR Kalite Yorumu
        quality = "Mükemmel" if snr > 40 else "İyi" if snr > 25 else "Orta" if snr > 10 else "Kötü"
        
        # Kanal Frekansı Tahmini
        freq = "2.4 GHz" if channel <= 14 else "5 GHz"
        
        rf_text = f"""
 [RF PARAMETRELERİ]
 ====================================
 Kanal         : {channel} ({freq})
 Kanal Genişliği: {net.get('channel_width', 20)} MHz
 PHY Standardı : {net.get('phy_type', '802.11n')}
 
 [SİNYAL KALİTESİ]
 ====================================
 Sinyal (RSSI) : {rssi} dBm
 Gürültü (Noise): {noise} dBm
 SNR Değeri    : {snr} dB ({quality})
        """
        self.txt_rf.delete('1.0', 'end')
        self.txt_rf.insert('end', rf_text)

        # --- 3. SEKME: GÜVENLİK ---
        crypto = net.get('crypto', 'Open')
        wps_status = "AÇIK (RİSKLİ!)" if net.get('wps_enabled') else "Kapalı"
        
        # Zafiyet Analizi
        vulns = []
        if "Open" in crypto or "WEP" in crypto:
            vulns.append("-> Aircrack-ng ile şifresiz dinleme mümkün")
            vulns.append("-> Man-in-the-Middle (MITM) saldırılarına açık")
        if net.get('wps_enabled'):
            vulns.append("-> WPS PIN saldırıları (Reaver/Pixie Dust) mümkün")
        if "WPA2" in crypto:
            vulns.append("-> Handshake yakalama (Deauth Attack) mümkün")
            vulns.append("-> Sözlük saldırıları (Brute-force) denenebilir")
        
        if not vulns: vulns.append("-> Bilinen doğrudan bir zafiyet yok.")

        # Evil Twin Kontrolü
        rogue_status = "Temiz"
        try:
            if self.rogue_detect and self.rogue_detect.is_evil_twin(net):
                rogue_status = "!!! KRİTİK: EVIL TWIN ŞÜPHESİ !!!"
        except: pass

        sec_text = f"""
 [GÜVENLİK YAPILANDIRMASI]
 ====================================
 Protokol      : {crypto}
 WPS Durumu    : {wps_status}
 Rogue Durumu  : {rogue_status}
 
 [RİSK ANALİZİ]
 ====================================
 Risk Skoru    : %{int(risk_score * 100)}
 
 [SALDIRI YÜZEYİ]
 ------------------------------------
 {chr(10).join(vulns)}
        """
        self.txt_sec.delete('1.0', 'end')
        self.txt_sec.insert('end', sec_text)

        # --- 4. SEKME: CİHAZLAR ---
        self.client_tree.delete(*self.client_tree.get_children())
        clients = self.db.query("SELECT * FROM clients WHERE bssid_connected=?", (self.current_bssid,))
        
        if clients:
            for c in clients:
                cli = dict(c)
                self.client_tree.insert('', 'end', values=(
                    cli.get('mac'),
                    cli.get('vendor', 'Bilinmiyor'),
                    cli.get('device_type', 'Diğer'),
                    f"{cli.get('rssi', -100)} dBm"
                ))
        
        # --- 5. SEKME: GRAFİK GÜNCELLEME ---
        if rssi: self.mini_rssi.update_rssi(rssi)