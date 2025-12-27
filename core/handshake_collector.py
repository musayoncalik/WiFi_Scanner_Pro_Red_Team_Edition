import logging
from scapy.all import EAPOL, Dot11
from utils.helpers import db_now

log = logging.getLogger(__name__)

class HandshakeCollector:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
        self.pmkid_cache = set()
    
    def _extract_pmkid(self, pkt):
        try:
            if not pkt.haslayer(EAPOL):
                return None
            
            eapol = pkt[EAPOL]
            if not hasattr(eapol, 'key_data') or not eapol.key_data:
                return None
            
            key_data = bytes(eapol.key_data)
            if len(key_data) >= 16:
                pmkid = key_data[:16].hex()
                return pmkid
        except Exception:
            pass
        return None
    
    def process_frame(self, pkt):
        try:
            if not pkt.haslayer(Dot11) or not pkt.haslayer(EAPOL):
                return
            
            bssid = getattr(pkt, 'addr3', None) or getattr(pkt, 'addr1', None) or 'unknown'
            ts = db_now()
            
            pmkid = self._extract_pmkid(pkt)
            if pmkid:
                cache_key = f"{bssid}:{pmkid}"
                if cache_key not in self.pmkid_cache:
                    self.pmkid_cache.add(cache_key)
                    self.db.execute(
                        "INSERT INTO recommendations (ts, target, recommendation) VALUES (?,?,?)",
                        (ts, bssid, f"PMKID tespit edildi: {pmkid[:16]}...")
                    )
                    log.info("PMKID tespit edildi: %s -> %s", bssid, pmkid[:16])
            
            self.db.execute(
                "INSERT INTO recommendations (ts, target, recommendation) VALUES (?,?,?)",
                (ts, bssid, "EAPOL frame gözlemlendi - handshake fragment")
            )
            log.debug("EAPOL gözlemlendi: %s", bssid)
            
        except Exception:
            log.exception("HandshakeCollector işleme hatası")
