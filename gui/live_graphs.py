import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import time
from collections import deque

# Modern Renk Paleti
MODERN_COLORS = {
    'primary': '#6366f1',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'purple': '#8b5cf6',
    'pink': '#ec4899',
    'cyan': '#06b6d4',
}

class LiveGraph:
    
    def __init__(self, parent, title="Grafik", max_points=60, color=None):
        self.frame = tk.Frame(parent, bg='white')
        self.fig = Figure(figsize=(5, 3), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111, facecolor='#f8fafc')
        
        self.title = title
        self.color = color or MODERN_COLORS['primary']
        self.max_points = max_points
        
        self.x = deque(maxlen=max_points)
        self.y = deque(maxlen=max_points)
        
        # Başlık ayarı
        if title:
            self.ax.set_title(title, fontsize=9, fontweight='bold', pad=5, color='#334155')
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # İlk boş çizim
        self._setup_ax()

    def _setup_ax(self):
        """Grafik eksen ve stil ayarları"""
        self.ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#cbd5e1')
        self.ax.spines['bottom'].set_color('#cbd5e1')
        self.ax.tick_params(axis='both', colors='#64748b', labelsize=8)

    def update(self, new_x, new_y):
        self.x.append(new_x)
        self.y.append(new_y)
        
        self.ax.clear()
        self.ax.set_facecolor('#f8fafc')
        
        # Çizgi ve Dolgu
        self.ax.plot(list(self.x), list(self.y), 
                     linewidth=1.5, 
                     color=self.color,
                     marker='o',
                     markersize=2)
                     
        self.ax.fill_between(list(self.x), list(self.y), 
                             alpha=0.1, 
                             color=self.color)
        
        # Başlığı ve stili koru (clear() sildiği için tekrar ayarla)
        if self.title:
            self.ax.set_title(self.title, fontsize=9, fontweight='bold', pad=5, color='#334155')
        
        self._setup_ax()
        self.canvas.draw()

class RSSIGraph(LiveGraph):
    # DÜZELTME: Artık title ve max_points parametrelerini kabul ediyor!
    def __init__(self, parent, title="RSSI Sinyal Gücü", max_points=60):
        super().__init__(parent, title, max_points, color=MODERN_COLORS['info'])
        self.ax.set_ylabel("dBm", fontsize=8, color='#64748b')
        self.ax.set_ylim(-100, -20)
    
    def update_rssi(self, rssi):
        if rssi is not None:
            # X ekseni için zaman yerine sadece sayı sayacı kullanabiliriz 
            # veya şimdiki zamanı kullanabiliriz.
            self.update(time.time(), rssi)
            # Y eksenini sabitle
            self.ax.set_ylim(-100, -20)
            # X ekseninde etiketleri gizle (daha temiz görünüm için)
            self.ax.set_xticklabels([])

class ChannelHeatmap:
    
    def __init__(self, parent, title="Kanal Yoğunluğu"):
        self.frame = tk.Frame(parent, bg='white')
        self.fig = Figure(figsize=(5, 3), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111, facecolor='#f8fafc')
        
        self.title = title
        if title:
            self.ax.set_title(title, fontsize=9, fontweight='bold', pad=5, color='#334155')
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.channels = list(range(1, 15))
        
        self._setup_ax()

    def _setup_ax(self):
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#cbd5e1')
        self.ax.spines['bottom'].set_color('#cbd5e1')
        self.ax.tick_params(axis='both', colors='#64748b', labelsize=8)
        self.ax.set_xticks(self.channels)
        self.ax.set_xlim(0.5, 14.5)

    def update(self, channel_data):
        self.ax.clear()
        self.ax.set_facecolor('#f8fafc')
        
        counts = [channel_data.get(ch, 0) for ch in range(1, 15)]
        
        # Renkler
        colors = []
        for c in counts:
            if c == 0: colors.append('#e2e8f0')
            elif c < 3: colors.append(MODERN_COLORS['success'])
            elif c < 6: colors.append(MODERN_COLORS['warning'])
            else: colors.append(MODERN_COLORS['danger'])
            
        bars = self.ax.bar(self.channels, counts, color=colors, width=0.6)
        
        # Değerleri yaz
        for bar, count in zip(bars, counts):
            if count > 0:
                self.ax.text(bar.get_x() + bar.get_width()/2, 
                             bar.get_height() + 0.1, 
                             str(int(count)), 
                             ha='center', va='bottom', fontsize=7, fontweight='bold')
        
        if self.title:
            self.ax.set_title(self.title, fontsize=9, fontweight='bold', pad=5, color='#334155')
            
        self._setup_ax()
        self.canvas.draw()

class TrafficGraph(LiveGraph):
    
    def __init__(self, parent, max_points=60):
        super().__init__(parent, "Frame Trafiği", max_points, color=MODERN_COLORS['purple'])
        self.ax.set_ylabel("Paket/sn", fontsize=8, color='#64748b')
    
    def update_traffic(self, frame_count):
        self.update(time.time(), frame_count)
        self.ax.set_xticklabels([]) # Zamanı gizle