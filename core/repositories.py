from typing import Optional, List, Dict, Any
from core.interfaces import IRepository
from utils.db import Database

class NetworkRepository(IRepository):
    def __init__(self, db: Database):
        self.db = db
    
    def save(self, entity: Dict[str, Any]) -> bool:
        try:
            self.db.execute(
                """INSERT OR REPLACE INTO networks 
                   (bssid, ssid, channel, crypto, last_seen, vendor, rssi)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (entity.get('bssid'), entity.get('ssid'), entity.get('channel'),
                 entity.get('crypto'), entity.get('last_seen'), entity.get('vendor'),
                 entity.get('rssi'))
            )
            return True
        except Exception:
            return False
    
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM networks WHERE bssid = ?", (entity_id,))
        if rows:
            return dict(rows[0])
        return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM networks ORDER BY last_seen DESC")
        return [dict(r) for r in rows]
    
    def find_by_channel(self, channel: int) -> List[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM networks WHERE channel = ?", (channel,))
        return [dict(r) for r in rows]
    
    def find_by_crypto(self, crypto: str) -> List[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM networks WHERE crypto = ?", (crypto,))
        return [dict(r) for r in rows]

class FrameRepository(IRepository):
    def __init__(self, db: Database):
        self.db = db
    
    def save(self, entity: Dict[str, Any]) -> bool:
        try:
            self.db.execute(
                "INSERT OR IGNORE INTO frames (ts, type, subtype, src, dst, bssid, rssi, raw) VALUES (?,?,?,?,?,?,?,?)",
                (entity.get('ts'), entity.get('type'), entity.get('subtype'),
                 entity.get('src'), entity.get('dst'), entity.get('bssid'),
                 entity.get('rssi'), entity.get('raw'))
            )
            return True
        except Exception:
            return False
    
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM frames WHERE id = ?", (int(entity_id),))
        if rows:
            return dict(rows[0])
        return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM frames ORDER BY ts DESC LIMIT 1000")
        return [dict(r) for r in rows]
    
    def count_by_subtype(self, subtype: str, window_seconds: int) -> int:
        from utils.helpers import db_now
        now = db_now()
        rows = self.db.query(
            "SELECT COUNT(*) as c FROM frames WHERE subtype=? AND ts>?",
            (subtype, now - window_seconds)
        )
        return rows[0]['c'] if rows else 0

class IDSEventRepository(IRepository):
    def __init__(self, db: Database):
        self.db = db
    
    def save(self, entity: Dict[str, Any]) -> bool:
        try:
            self.db.execute(
                "INSERT INTO ids_events (ts, event_type, description, data) VALUES (?,?,?,?)",
                (entity.get('ts'), entity.get('event_type'), entity.get('description'),
                 entity.get('data'))
            )
            return True
        except Exception:
            return False
    
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM ids_events WHERE id = ?", (int(entity_id),))
        if rows:
            return dict(rows[0])
        return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM ids_events ORDER BY ts DESC LIMIT 100")
        return [dict(r) for r in rows]
    
    def find_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM ids_events WHERE event_type = ? ORDER BY ts DESC", (event_type,))
        return [dict(r) for r in rows]

