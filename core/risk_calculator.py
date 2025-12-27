import logging
from core.rogue_ap_detector import RogueAPDetector

log = logging.getLogger(__name__)

class RiskCalculator:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
        self.rogue_detector = RogueAPDetector(db, config)
    
    def calculate_network_risk(self, network_data):
        """Ağ için risk skoru hesapla (0.0 - 1.0)"""
        risk_score = 0.0
        
        # Verileri güvenli şekilde al
        crypto = str(network_data.get('crypto', 'Open'))
        ssid = str(network_data.get('ssid', ''))
        
        # 1. Şifreleme Protokolü Riski (En Kritik)
        if 'Open' in crypto or 'Güvensiz' in crypto:
            risk_score = 1.0  # Şifresiz ağ = Kırmızı Alarm
        elif 'WEP' in crypto:
            risk_score = 0.9  # WEP çok kolay kırılır
        elif 'WPA' in crypto and 'WPA2' not in crypto and 'WPA3' not in crypto:
            risk_score = 0.7  # Eski WPA (TKIP) risklidir
        elif 'WPA2' in crypto:
            if 'TKIP' in crypto:
                risk_score = 0.5  # WPA2 ama eski şifreleme kullanıyor
            else:
                risk_score = 0.2  # Standart WPA2-CCMP (Güvenli sayılır)
        elif 'WPA3' in crypto:
            risk_score = 0.0  # En güvenli standart
        
        # 2. Ekstra Risk Faktörleri
        if 'WPS Açık' in crypto:
            risk_score = min(risk_score + 0.2, 1.0) # WPS Brute-force riski
            
        if 'PMF' not in crypto and 'WPA3' not in crypto:
            # PMF (Management Frame Protection) yoksa Deauth saldırısına açıktır
            risk_score = min(risk_score + 0.1, 1.0)
        
        # 3. Gizli Ağ Riski
        # Yeni scanner.py "<GIZLI AG>" etiketini kullanıyor, onu yakalayalım
        if ssid == "<GIZLI AG>" or not ssid:
            risk_score = min(risk_score + 0.15, 1.0) 
        
        # 4. Rogue AP (Evil Twin) Riski
        if ssid and ssid != "<GIZLI AG>":
            try:
                evil_twin_risk = self.rogue_detector.get_evil_twin_risk(ssid)
                risk_score = max(risk_score, evil_twin_risk)
            except:
                pass
        
        return round(min(risk_score, 1.0), 2)
    
    def get_risk_label(self, risk_score):
        """Risk skoruna göre etiket döndür"""
        if risk_score >= 0.8: return "Yüksek Risk"
        elif risk_score >= 0.5: return "Orta Risk"
        elif risk_score >= 0.2: return "Düşük Risk"
        else: return "Güvenli"
    
    def get_risk_color(self, risk_score):
        """Risk skoruna göre renk döndür (hex)"""
        # Arayüzdeki renklerle uyumlu tonlar
        if risk_score >= 0.8: return "#ef4444"  # Kırmızı (Danger)
        elif risk_score >= 0.5: return "#f59e0b"  # Turuncu (Warning)
        elif risk_score >= 0.2: return "#facc15"  # Sarı
        else: return "#10b981"  # Yeşil (Success)