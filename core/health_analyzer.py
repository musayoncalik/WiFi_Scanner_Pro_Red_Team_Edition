import logging
import time

log = logging.getLogger(__name__)

class HealthAnalyzer:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
    
    def airtime_estimate(self, channel=None, window_seconds=60):
        now = int(time.time())
        query = "SELECT COUNT(*) as c FROM frames WHERE ts > ?"
        params = [now - window_seconds]
        
        if channel:
            query += " AND bssid IN (SELECT bssid FROM networks WHERE channel = ?)"
            params.append(channel)
        
        rows = self.db.query(query, tuple(params))
        total = rows[0]['c'] if rows else 0
        
        airtime_score = min(100, int(total / window_seconds))
        
        return {
            "frames_in_window": total,
            "airtime_score": airtime_score,
            "window_seconds": window_seconds
        }
    
    def retry_rate(self, window_seconds=60):
        now = int(time.time())
        rows = self.db.query(
            "SELECT COUNT(*) as c FROM frames WHERE ts > ? AND subtype = ?",
            (now - window_seconds, '11')
        )
        retry_count = rows[0]['c'] if rows else 0
        
        total_rows = self.db.query(
            "SELECT COUNT(*) as c FROM frames WHERE ts > ?",
            (now - window_seconds,)
        )
        total = total_rows[0]['c'] if total_rows else 1
        
        retry_percentage = (retry_count / total * 100) if total > 0 else 0
        
        return {
            "retry_count": retry_count,
            "total_frames": total,
            "retry_percentage": round(retry_percentage, 2)
        }
