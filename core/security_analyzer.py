import logging
from scapy.all import Dot11Elt
from utils.helpers import db_now

log = logging.getLogger(__name__)

class SecurityAnalyzer:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
        self._processed_findings = set()
    
    def _extract_ies(self, pkt):
        ies = []
        if not pkt.haslayer(Dot11Elt):
            return ies
        
        elt = pkt[Dot11Elt]
        while elt:
            info = elt.info if hasattr(elt, 'info') else b''
            ies.append((elt.ID, info))
            elt = elt.payload.getlayer(Dot11Elt)
        return ies
    
    def analyze_frame(self, pkt):
        try:
            ies = self._extract_ies(pkt)
            if not ies:
                return
            
            bssid = getattr(pkt, 'addr3', None) or getattr(pkt, 'addr1', None) or 'unknown'
            findings = []
            
            for ie_id, info in ies:
                if ie_id == 221 and b'WPS' in info:
                    finding = f"WPS etkin (vendor IE) - {bssid}"
                    if finding not in self._processed_findings:
                        findings.append("WPS tespit edildi (güvenlik riski)")
                        self._processed_findings.add(finding)
                
                if ie_id == 48:
                    finding = f"RSN IE mevcut - {bssid}"
                    if finding not in self._processed_findings:
                        findings.append("RSN IE tespit edildi (WPA2/WPA3)")
                        self._processed_findings.add(finding)
            
            if findings:
                for f in findings:
                    self.db.execute(
                        "INSERT INTO recommendations (ts, target, recommendation) VALUES (?,?,?)",
                        (db_now(), bssid, f)
                    )
            
        except Exception:
            log.exception("Güvenlik analizi hatası")
