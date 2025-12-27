import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
# Grafik çizimi sırasında GUI'nin donmasını önlemek için sessiz mod (Backend ayarı)
matplotlib.use('Agg') 
from gui.styles import apply_style, COLORS, FONTS, get_risk_bg_color
from gui.live_graphs import RSSIGraph, ChannelHeatmap, TrafficGraph
from gui.popup import notify_async
from gui.detail_panel import DetailPanel
import threading
import time
import logging
import os
import subprocess
import glob

log = logging.getLogger(__name__)

# --- 1. NETWORK FILTER SINIFI ---
class NetworkFilter:
    def __init__(self):
        self.vendor_filter = None
        self.band_filter = None
        self.security_filter = None
        self.rssi_min = None
        self.rssi_max = None
    
    def apply(self, networks):
        filtered = networks
        # Üretici Filtresi
        if self.vendor_filter:
            filtered = [n for n in filtered if self.vendor_filter.lower() in (n.get('vendor') or '').lower()]
        
        # Band Filtresi (2.4GHz / 5GHz)
        if self.band_filter:
            if self.band_filter == '2.4GHz':
                filtered = [n for n in filtered if n.get('channel') and 1 <= int(n.get('channel')) <= 14]
            elif self.band_filter == '5GHz':
                filtered = [n for n in filtered if n.get('channel') and int(n.get('channel')) > 14]
        
        # Güvenlik Filtresi
        if self.security_filter:
            filtered = [n for n in filtered if n.get('crypto') == self.security_filter]
        
        # RSSI Filtreleri
        if self.rssi_min is not None:
            filtered = [n for n in filtered if n.get('rssi') and n.get('rssi') >= self.rssi_min]
        if self.rssi_max is not None:
            filtered = [n for n in filtered if n.get('rssi') and n.get('rssi') <= self.rssi_max]
            
        return filtered

# --- 2. ANA UYGULAMA ---
class WifiGuiApp:
    def __init__(self, db, scanner, ids, config, event_bus=None):
        self.db = db
        self.scanner = scanner
        self.ids = ids
        self.config = config
        self.event_bus = event_bus
        self.filter = NetworkFilter()
        
        # Analiz Araçlarını Yükle
        try:
            from core.channel_analyzer import ChannelAnalyzer
            from core.health_analyzer import HealthAnalyzer
            from core.recommendation_engine import RecommendationEngine
            from core.snr_analyzer import SNRAnalyzer
            from core.rogue_ap_detector import RogueAPDetector
            from core.risk_calculator import RiskCalculator
            
            # Red Team Modülleri (Varsa yükle, yoksa geç)
            try:
                from core.autopilot import AutoPilot
                from core.attacker import Attacker
                self.attacker = Attacker(self.scanner.iface)
                self.autopilot = AutoPilot(self.db, self.scanner, self.attacker, self.ids)
            except ImportError:
                self.attacker = None
                self.autopilot = None
                log.warning("Red Team modülleri eksik, saldırı özellikleri devre dışı.")

            self.channel_analyzer = ChannelAnalyzer(db, config)
            self.health_analyzer = HealthAnalyzer(db, config)
            self.recommendation_engine = RecommendationEngine(db, config)
            self.snr_analyzer = SNRAnalyzer(db, config)
            self.rogue_detector = RogueAPDetector(db, config)
            self.risk_calculator = RiskCalculator(db, config)
            
        except Exception as e:
            log.error(f"Modül yükleme hatası: {e}")
        
        # Pencere Ayarları
        self.root = tk.Tk()
        self.root.title("🔍 WiFi Scanner Pro - Red Team Edition")
        self.root.geometry("1400x850")
        
        # Modern Temayı Uygula
        apply_style(self.root)
        
        # Ana Notebook (Sekmeler)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.refresh_interval = 2000 # 2 saniye
        self._stop = False
        
        # Sekmeleri Oluştur
        self._build_tabs()
        
        # Asenkron GUI Yenileme Döngüsünü Başlat
        self.root.after(1000, self._ui_refresh_loop)

    def _build_tabs(self):
        """Tüm sekmeleri inşa eder"""
        self._build_main_tab()
        self._build_captures_tab()
        self._build_live_graphs_tab()
        self._build_security_tab()
        self._build_ids_tab()
        self._build_reports_tab()
        self._build_settings_tab()

    # --- 1. MAIN TAB (Ana Ekran) ---
    def _build_main_tab(self):
        self.tab_main = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_main, text="🏠 Ana Ekran")
        
        header_frame = tk.Frame(self.tab_main, bg=COLORS['bg_secondary'], height=60)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))

        # Auto Pilot Butonu
        if self.autopilot:
            self.auto_mode_var = tk.BooleanVar(value=False)
            self.auto_btn = tk.Checkbutton(header_frame, text="🤖 AUTO-PWN MODE", 
                                       variable=self.auto_mode_var, 
                                       command=self._toggle_autopilot,
                                       bg=COLORS['bg_secondary'], fg="red", font=("Arial", 10, "bold"))
            self.auto_btn.pack(side='right', padx=20)
        
        tk.Label(header_frame, text="📡 WiFi Tehdit Analizi", font=FONTS['heading'], bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side='left', padx=15, pady=15)
        self.stats_frame = tk.Frame(header_frame, bg=COLORS['bg_secondary'])
        self.stats_frame.pack(side='right', padx=15, pady=15)

        btn_frame = tk.Frame(header_frame, bg=COLORS['bg_secondary'])
        btn_frame.pack(side='right', padx=10)
        tk.Button(btn_frame, text="🧹 Temizle", bg=COLORS['warning'], fg='white', font=('Inter', 9, 'bold'), relief='flat', padx=10, pady=5, command=self._reset_data).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🚪 Çıkış", bg=COLORS['danger'], fg='white', font=('Inter', 9, 'bold'), relief='flat', padx=10, pady=5, command=self._quit_app).pack(side='left', padx=5)

        # Filtreler
        filter_frame = ttk.LabelFrame(self.tab_main, text="🔍 Filtreler", padding=10)
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Üretici:").grid(row=0, column=0, padx=5)
        self.vendor_entry = ttk.Entry(filter_frame, width=15)
        self.vendor_entry.grid(row=0, column=1, padx=5)
        self.vendor_entry.bind('<KeyRelease>', lambda e: self._apply_filters())
        
        ttk.Label(filter_frame, text="Güvenlik:").grid(row=0, column=2, padx=5)
        self.security_combo = ttk.Combobox(filter_frame, values=['', 'Open', 'WPA', 'WPA2', 'WPA3'], width=10, state='readonly')
        self.security_combo.grid(row=0, column=3, padx=5)
        self.security_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())

        ttk.Button(filter_frame, text="Temizle", command=self._clear_filters).grid(row=0, column=6, padx=10)

        # Liste
        self.main_paned = ttk.PanedWindow(self.tab_main, orient='horizontal')
        self.main_paned.pack(fill='both', expand=True, padx=5, pady=5)
        list_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(list_frame, weight=1)
        
        columns = ("bssid", "ssid", "kanal", "nesil", "güvenlik", "rssi", "üretici", "risk")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        headers = {
            "bssid": "🆔 BSSID", "ssid": "📡 SSID", "kanal": "📶 CH", 
            "nesil": "🚀 NESİL", "güvenlik": "🔒 Sec", "rssi": "📊 dBm", 
            "üretici": "🏭 Vendor", "risk": "⚠️ Risk"
        }
        for col in columns:
            self.tree.heading(col, text=headers.get(col, col.upper()))
            self.tree.column(col, width=90, anchor='center')
        
        self.tree.column("ssid", width=180, anchor='w')
        self.tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind("<Double-1>", self.on_row_double)
        self.tree.bind("<Button-3>", self.on_right_click)

    # --- 2. CAPTURES TAB (Yakalananlar) ---
    def _build_captures_tab(self):
        self.tab_captures = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_captures, text="🗂️ Yakalananlar")
        
        top_frame = ttk.Frame(self.tab_captures)
        top_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(top_frame, text="Handshake Veritabanı (.cap)", font=("Arial", 12, "bold")).pack(side='left')
        ttk.Button(top_frame, text="🔄 Listeyi Yenile", command=self._refresh_capture_list).pack(side='right')
        
        list_frame = ttk.LabelFrame(self.tab_captures, text="Kayıtlı Dosyalar", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ("dosya", "boyut", "tarih", "hedef")
        self.cap_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.cap_tree.heading("dosya", text="Dosya Adı"); self.cap_tree.column("dosya", width=250)
        self.cap_tree.heading("boyut", text="Boyut"); self.cap_tree.column("boyut", width=80)
        self.cap_tree.heading("tarih", text="Tarih"); self.cap_tree.column("tarih", width=150)
        self.cap_tree.heading("hedef", text="Hedef BSSID")
        
        self.cap_tree.pack(side='left', fill='both', expand=True)
        
        btn_frame = ttk.Frame(self.tab_captures)
        btn_frame.pack(fill='x', padx=10, pady=10)
        ttk.Button(btn_frame, text="📂 Klasörü Göster", command=self._open_capture_folder).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Seçileni Sil", command=self._delete_capture).pack(side='left', padx=5)

    def _refresh_capture_list(self):
        self.cap_tree.delete(*self.cap_tree.get_children())
        cap_path = "captures/handshakes"
        if not os.path.exists(cap_path): os.makedirs(cap_path, exist_ok=True); return
        files = glob.glob(os.path.join(cap_path, "*.cap"))
        files.sort(key=os.path.getmtime, reverse=True)
        for f in files:
            name = os.path.basename(f)
            size = f"{os.path.getsize(f) / 1024:.1f} KB"
            date = time.strftime('%d/%m/%Y %H:%M', time.localtime(os.path.getmtime(f)))
            target = name.split('_')[1].replace('-', ':') if '_' in name else "Bilinmiyor"
            self.cap_tree.insert('', 'end', values=(name, size, date, target))

    def _open_capture_folder(self):
        path = os.path.abspath("captures/handshakes")
        if os.name == 'nt': os.startfile(path)
        else: subprocess.Popen(['xdg-open', path])

    def _delete_capture(self):
        selected = self.cap_tree.selection()
        if not selected: return
        filename = self.cap_tree.item(selected)['values'][0]
        if messagebox.askyesno("Onay", f"{filename} silinsin mi?"):
            os.remove(os.path.join("captures/handshakes", filename))
            self._refresh_capture_list()

    # --- 3. LIVE GRAPHS TAB ---
    def _build_live_graphs_tab(self):
        self.tab_live = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_live, text="📈 Canlı Grafikler")
        rssi_frame = ttk.LabelFrame(self.tab_live, text="RSSI Sinyal Gücü", padding=5)
        rssi_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.rssi_graph = RSSIGraph(rssi_frame)
        self.rssi_graph.frame.pack(fill='both', expand=True)
        
        bottom_frame = ttk.Frame(self.tab_live)
        bottom_frame.pack(fill='both', expand=True, padx=5, pady=5)
        heatmap_frame = ttk.LabelFrame(bottom_frame, text="Kanal Yoğunluk", padding=5)
        heatmap_frame.pack(side='left', fill='both', expand=True, padx=5)
        self.heatmap = ChannelHeatmap(heatmap_frame)
        self.heatmap.frame.pack(fill='both', expand=True)
        
        traffic_frame = ttk.LabelFrame(bottom_frame, text="Trafik", padding=5)
        traffic_frame.pack(side='right', fill='both', expand=True, padx=5)
        self.traffic_graph = TrafficGraph(traffic_frame)
        self.traffic_graph.frame.pack(fill='both', expand=True)

    # --- 4. SECURITY TAB ---
    def _build_security_tab(self):
        self.tab_security = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_security, text="🔒 Güvenlik")
        top_frame = ttk.Frame(self.tab_security)
        top_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        snr_frame = ttk.LabelFrame(top_frame, text="SNR Analizi", padding=10)
        snr_frame.pack(side='left', fill='both', expand=True, padx=5)
        columns_snr = ("bssid", "kanal", "rssi", "snr", "noise")
        self.snr_tree = ttk.Treeview(snr_frame, columns=columns_snr, show='headings', height=10)
        for col in columns_snr: self.snr_tree.heading(col, text=col.upper()); self.snr_tree.column(col, width=100)
        self.snr_tree.pack(fill='both', expand=True)

        overlap_frame = ttk.LabelFrame(top_frame, text="Kanal Overlap", padding=10)
        overlap_frame.pack(side='right', fill='both', expand=True, padx=5)
        self.overlap_text = tk.Text(overlap_frame, height=10, width=40, wrap='word')
        self.overlap_text.pack(fill='both', expand=True)
        
        rec_frame = ttk.LabelFrame(self.tab_security, text="Güvenlik Önerileri", padding=10)
        rec_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.security_text = tk.Text(rec_frame, height=10)
        self.security_text.pack(fill='both', expand=True)
        
        btn_frame = ttk.Frame(self.tab_security)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="🔄 Yenile", command=self._refresh_security).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🚨 Rogue AP Kontrol", command=self._check_rogue_aps).pack(side='left', padx=5)

    # --- 5. IDS TAB ---
    def _build_ids_tab(self):
        self.tab_ids = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ids, text="🚨 IDS Olayları")
        ids_frame = ttk.LabelFrame(self.tab_ids, text="Tespit Edilen Olaylar", padding=10)
        ids_frame.pack(fill='both', expand=True, padx=5, pady=5)
        columns = ("zaman", "tip", "açıklama")
        self.ids_tree = ttk.Treeview(ids_frame, columns=columns, show='headings')
        for col in columns: self.ids_tree.heading(col, text=col.upper()); self.ids_tree.column(col, width=150)
        self.ids_tree.pack(fill='both', expand=True)

    # --- 6. REPORTS TAB ---
    def _build_reports_tab(self):
        self.tab_reports = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reports, text="📄 Raporlar")
        frame = ttk.LabelFrame(self.tab_reports, text="Rapor Oluştur", padding=20)
        frame.pack(expand=True)
        ttk.Button(frame, text="PDF Rapor", command=self.gen_pdf).pack(pady=5)
        ttk.Button(frame, text="HTML Rapor", command=self.gen_html).pack(pady=5)
        ttk.Button(frame, text="CSV Dışa Aktar", command=self.gen_csv).pack(pady=5)

    # --- 7. SETTINGS TAB ---
    def _build_settings_tab(self):
        self.tab_settings = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_settings, text="⚙️ Ayarlar")
        f = ttk.LabelFrame(self.tab_settings, text="Tarayıcı Kontrolü", padding=20)
        f.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(f, text="Tarama Modu:").pack(anchor='w')
        self.scan_mode_var = tk.StringVar(value="Normal")
        ttk.Combobox(f, textvariable=self.scan_mode_var, values=["Hızlı", "Normal", "Gelişmiş", "Ultra"], state='readonly').pack(anchor='w', pady=5)
        ttk.Button(f, text="Uygula", command=self._save_settings).pack(anchor='w', pady=10)

    # --- RED TEAM MANTIĞI ---
    def _toggle_autopilot(self):
        if self.auto_mode_var.get():
            if messagebox.askyesno("Otonom Mod", "Aktif saldırı moduna geçilecek. Onaylıyor musunuz?"):
                self.autopilot.start()
                notify_async("AutoPilot", "Otonom mod aktif.")
            else:
                self.auto_mode_var.set(False)
        else:
            self.autopilot.stop()
            notify_async("AutoPilot", "Manuel moda geçildi.")

    def on_right_click(self, event):
        try:
            item = self.tree.identify_row(event.y)
            if item:
                self.tree.selection_set(item)
                values = self.tree.item(item)['values']
                bssid, channel = values[0], values[2]
                
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(label="🔍 Detaylı Analiz", command=lambda: self._show_network_details(bssid))
                menu.add_separator()
                menu.add_command(label="⚡ Deauth Saldırısı", command=lambda: self._start_deauth_attack(bssid, channel))
                menu.add_command(label="🤝 Handshake Yakala", command=lambda: self._trigger_handshake_capture(channel))
                menu.post(event.x_root, event.y_root)
        except: pass

    def _start_deauth_attack(self, bssid, channel):
        if not messagebox.askyesno("⚠️ UYARI", f"HEDEF: {bssid}\nBu işlem hedefi ağdan düşürecektir. Onaylıyor musunuz?"):
            return
            
        def run_attack():
            try:
                if hasattr(self.scanner, 'lock_channel') and str(channel).isdigit():
                    self.scanner.lock_channel(int(channel))
                
                if self.attacker:
                    notify_async("Saldırı", f"Hedef: {bssid}\nPaketler gönderiliyor...")
                    self.attacker.deauth_target(target_mac="ff:ff:ff:ff:ff:ff", gateway_mac=bssid, count=50)
                    notify_async("Bitti", "Saldırı tamamlandı.")
                else:
                    notify_async("Hata", "Attacker modülü yok.")
            except Exception as e:
                notify_async("Hata", f"{e}")

        threading.Thread(target=run_attack, daemon=True).start()

    def _trigger_handshake_capture(self, channel):
        if hasattr(self.scanner, 'lock_channel') and str(channel).isdigit():
            self.scanner.lock_channel(int(channel))
            notify_async("Handshake", f"Kanal {channel} kilitlendi. Bekleniyor...")

    # --- SİSTEM SIFIRLAMA (Düzeltildi) ---
    def _reset_data(self):
        if messagebox.askyesno("Sıfırla", "Tüm veriler temizlenecek ve tarama tazelenecek.\nEmin misiniz?"):
            try:
                tables = ["networks", "clients", "client_connections", "frames", "ids_events", "recommendations"]
                for table in tables: self.db.execute(f"DELETE FROM {table}")
                
                self.tree.delete(*self.tree.get_children())
                if hasattr(self, 'ids_tree'): self.ids_tree.delete(*self.ids_tree.get_children())
                if hasattr(self, 'snr_tree'): self.snr_tree.delete(*self.snr_tree.get_children())
                
                if hasattr(self.scanner, 'unlock_channel'): self.scanner.unlock_channel()
                if hasattr(self, 'detail_panel'): self.detail_panel.hide()
                self._clear_filters()
                
                notify_async("Sistem Sıfırlandı", "Veriler temizlendi.")
            except Exception as e: log.error(f"Sıfırlama hatası: {e}")

    # --- GUI REFRESH LOOP ---
    def _ui_refresh_loop(self):
        if self._stop: return
        try:
            self._refresh_network_list()
            self._refresh_live_graphs()
            self._refresh_security()
            if hasattr(self, 'detail_panel') and self.detail_panel.current_bssid:
                self.detail_panel.refresh()
            
            last_hs = self.db.query("SELECT target FROM ids_events WHERE event_type='HANDSHAKE' AND ts > ? LIMIT 1", (time.time() - 3,))
            if last_hs: notify_async("⚡ HANDSHAKE!", f"Hedef: {last_hs[0]['target']}")
            self._refresh_capture_list()
        except: pass
        self.root.after(self.refresh_interval, self._ui_refresh_loop)

    def _refresh_network_list(self):
        try:
            try:
                rows = self.db.query("SELECT bssid, ssid, channel, crypto, generation, rssi, vendor FROM networks ORDER BY last_seen DESC")
            except:
                rows = self.db.query("SELECT bssid, ssid, channel, crypto, rssi, vendor FROM networks ORDER BY last_seen DESC")
            
            networks = [dict(r) for r in rows]
            filtered = self.filter.apply(networks)
            self._update_stats(len(networks), len(filtered))
            self.tree.delete(*self.tree.get_children())
            
            for n in filtered:
                risk = self.risk_calculator.calculate_network_risk(n)
                gen = n.get('generation', 'Wi-Fi 4')
                self.tree.insert('', 'end', values=(
                    n.get('bssid'), n.get('ssid') or '🔒 (Gizli)', 
                    n.get('channel'), gen, n.get('crypto'), 
                    f"{n.get('rssi')} dBm", n.get('vendor'), 
                    f"⚠️ %{int(risk*100)}"
                ), tags=(f"{int(risk*10)*10}%",))
            
            for i in range(0, 101, 10):
                self.tree.tag_configure(f"{i}%", background=get_risk_bg_color(i/100.0))
        except: pass

    # --- DİĞER YARDIMCI FONKSİYONLAR ---
    def _refresh_live_graphs(self):
        try:
            res = self.db.query("SELECT rssi FROM networks WHERE rssi IS NOT NULL ORDER BY last_seen DESC LIMIT 1")
            if res: self.rssi_graph.update_rssi(res[0][0])
            self.heatmap.update(self.channel_analyzer.occupancy(60))
            now = int(time.time())
            rows = self.db.query("SELECT COUNT(*) as c FROM frames WHERE ts > ?", (now - 10,))
            self.traffic_graph.update_traffic(rows[0]['c'] if rows else 0)
        except: pass

    def _refresh_security(self):
        try:
            recs = self.db.query("SELECT ts, target, recommendation FROM recommendations ORDER BY ts DESC LIMIT 100")
            self.security_text.delete('1.0', 'end')
            for r in recs: self.security_text.insert('end', f"[{r['ts']}] {r['target']}: {r['recommendation']}\n")
            
            snr_data = self.snr_analyzer.get_all_networks_snr()
            self.snr_tree.delete(*self.snr_tree.get_children())
            for d in snr_data[:50]: self.snr_tree.insert('', 'end', values=(d.get('bssid',''), d.get('channel',''), d.get('rssi',''), d.get('snr',''), d.get('noise_floor','')))
            
            mat = self.channel_analyzer.calculate_overlap_matrix()
            self.overlap_text.delete('1.0', 'end')
            for ch, d in sorted(mat.items()):
                self.overlap_text.insert('end', f"CH {ch}: {d['networks']} ağ\n")
        except: pass
        
    def _check_rogue_aps(self):
        try:
            rogues = self.rogue_detector.check_and_alert()
            if rogues: notify_async("Rogue AP", f"{len(rogues)} tehdit bulundu!")
            else: notify_async("Güvenli", "Tehdit yok.")
        except: pass

    def _save_settings(self):
        if hasattr(self.scanner, 'set_scan_mode'):
            self.scanner.set_scan_mode(self.scan_mode_var.get())
            notify_async("Başarılı", "Mod güncellendi.")

    def _apply_filters(self): self._refresh_network_list()
    def _clear_filters(self): 
        self.vendor_entry.delete(0, 'end')
        self.security_combo.set('')
        self.filter = NetworkFilter()
        self._refresh_network_list()

    def _update_stats(self, t, f):
        for w in self.stats_frame.winfo_children(): w.destroy()
        tk.Label(self.stats_frame, text=f"📊 Toplam: {t} | Filtre: {f}", bg=COLORS['bg_secondary'], fg='white').pack()

    def on_row_double(self, event):
        item = self.tree.selection()
        if not item: return
        self._show_network_details(self.tree.item(item)['values'][0])

    def _show_network_details(self, bssid):
        if not hasattr(self, 'detail_panel'):
            self.detail_panel = DetailPanel(self.main_paned, self.db, self.risk_calculator, self.rogue_detector, self.snr_analyzer, self.channel_analyzer, self.scanner)
            self.main_paned.add(self.detail_panel.panel, weight=1)
        self.detail_panel.show(bssid)

    def gen_pdf(self): 
        from reports.pdf_report import PDFReport
        PDFReport(self.db).generate_summary(); notify_async("PDF", "Rapor oluşturuldu.")
    def gen_html(self): 
        from reports.html_report import HTMLReport
        HTMLReport(self.db).generate_summary(); notify_async("HTML", "Rapor oluşturuldu.")
    def gen_csv(self): 
        from reports.csv_export import CSVExport
        CSVExport(self.db).export_networks(); notify_async("CSV", "Dışa aktarıldı.")

    def _quit_app(self): self.on_close()
    def on_close(self): self._stop = True; self.root.destroy()
    def run(self): self.root.protocol("WM_DELETE_WINDOW", self.on_close); self.root.mainloop()