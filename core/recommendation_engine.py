import logging
from utils.helpers import db_now

log = logging.getLogger(__name__)

class RecommendationEngine:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
    
    def best_channel(self):
        rows = self.db.query("SELECT channel, COUNT(*) as c FROM networks WHERE channel IS NOT NULL GROUP BY channel")
        counts = {r['channel']: r['c'] for r in rows}
        
        if not counts:
            return "Yeterli veri yok"
        
        channels_24 = [ch for ch in range(1, 15) if ch in counts]
        if channels_24:
            best = min(channels_24, key=lambda ch: counts.get(ch, 0))
            count = counts.get(best, 0)
            rec = f"Önerilen kanal: {best} (en az ağ: {count})"
        else:
            best = min(counts.keys(), key=lambda ch: counts.get(ch, 0))
            count = counts.get(best, 0)
            rec = f"Önerilen kanal: {best} (en az ağ: {count})"
        
        self.db.execute(
            "INSERT INTO recommendations (ts, target, recommendation) VALUES (?,?,?)",
            (db_now(), 'channel', rec)
        )
        return rec
    
    def pmf_recommendation(self):
        rows = self.db.query(
            "SELECT bssid, ssid FROM networks WHERE crypto IS NULL OR crypto = '' OR crypto = 'Open'"
        )
        if rows:
            networks = [f"{r['ssid'] or r['bssid']}" for r in rows[:5]]
            rec = f"PMF/WPA2+ etkinleştirilmesi önerilen ağlar: {', '.join(networks)}"
            self.db.execute(
                "INSERT INTO recommendations (ts, target, recommendation) VALUES (?,?,?)",
                (db_now(), 'pmf', rec)
            )
            return rec
        return "Tüm ağlar güvenlik protokolü kullanıyor"
    
    def weak_security_recommendation(self):
        rows = self.db.query(
            "SELECT bssid, ssid, crypto FROM networks WHERE crypto = 'Open' OR crypto = 'WPA'"
        )
        if rows:
            networks = [f"{r['ssid'] or r['bssid']} ({r['crypto']})" for r in rows[:10]]
            rec = f"Zayıf güvenlikli ağlar: {', '.join(networks)}"
            self.db.execute(
                "INSERT INTO recommendations (ts, target, recommendation) VALUES (?,?,?)",
                (db_now(), 'security', rec)
            )
            return rec
        return "Zayıf güvenlikli ağ tespit edilmedi"
