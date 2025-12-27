import logging
import time

log = logging.getLogger(__name__)

class SNRAnalyzer:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
        self.noise_floor_default = config.getint('snr', 'noise_floor_default', fallback=-95)
        self.window_seconds = config.getint('snr', 'window_seconds', fallback=60)
    
    def calculate_noise_floor(self, channel=None, window_seconds=None):
        window = window_seconds or self.window_seconds
        now = int(time.time())
        
        query = """
            SELECT MIN(rssi) as min_rssi 
            FROM frames 
            WHERE ts > ? AND rssi IS NOT NULL
        """
        params = [now - window]
        
        if channel:
            query += " AND bssid IN (SELECT bssid FROM networks WHERE channel = ?)"
            params.append(channel)
        
        rows = self.db.query(query, tuple(params))
        min_rssi = rows[0]['min_rssi'] if rows and rows[0]['min_rssi'] else self.noise_floor_default
        
        return min_rssi
    
    def calculate_snr(self, rssi, noise_floor=None, channel=None):
        if rssi is None:
            return None
        
        if noise_floor is None:
            noise_floor = self.calculate_noise_floor(channel)
        
        snr = rssi - noise_floor
        return round(snr, 2)
    
    def get_network_snr(self, bssid, window_seconds=None):
        window = window_seconds or self.window_seconds
        now = int(time.time())
        
        net_rows = self.db.query(
            "SELECT channel, rssi FROM networks WHERE bssid = ?",
            (bssid,)
        )
        if not net_rows:
            return None
        
        channel = net_rows[0]['channel']
        avg_rssi = net_rows[0]['rssi']
        
        rssi_rows = self.db.query(
            """
            SELECT AVG(rssi) as avg_rssi 
            FROM frames 
            WHERE bssid = ? AND ts > ? AND rssi IS NOT NULL
            """,
            (bssid, now - window)
        )
        
        if rssi_rows and rssi_rows[0]['avg_rssi']:
            avg_rssi = round(rssi_rows[0]['avg_rssi'], 2)
        
        noise_floor = self.calculate_noise_floor(channel, window)
        snr = self.calculate_snr(avg_rssi, noise_floor, channel)
        
        return {
            'bssid': bssid,
            'channel': channel,
            'rssi': avg_rssi,
            'noise_floor': noise_floor,
            'snr': snr
        }
    
    def get_all_networks_snr(self, window_seconds=None):
        window = window_seconds or self.window_seconds
        networks = self.db.query(
            "SELECT DISTINCT bssid FROM networks WHERE bssid IS NOT NULL"
        )
        
        results = []
        for net in networks:
            snr_info = self.get_network_snr(net['bssid'], window)
            if snr_info:
                results.append(snr_info)
        
        return results
