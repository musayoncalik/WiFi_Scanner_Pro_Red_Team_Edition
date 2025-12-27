import logging
import time

log = logging.getLogger(__name__)

DFS_CHANNELS_5GHZ = {
    52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144
}

CHANNEL_OVERLAP_24 = {
    1: {1, 2, 3, 4, 5},
    2: {1, 2, 3, 4, 5, 6},
    3: {1, 2, 3, 4, 5, 6, 7},
    4: {1, 2, 3, 4, 5, 6, 7, 8},
    5: {1, 2, 3, 4, 5, 6, 7, 8, 9},
    6: {2, 3, 4, 5, 6, 7, 8, 9, 10},
    7: {3, 4, 5, 6, 7, 8, 9, 10, 11},
    8: {4, 5, 6, 7, 8, 9, 10, 11},
    9: {5, 6, 7, 8, 9, 10, 11},
    10: {6, 7, 8, 9, 10, 11},
    11: {7, 8, 9, 10, 11},
    12: {8, 9, 10, 11, 12, 13},
    13: {9, 10, 11, 12, 13, 14},
    14: {10, 11, 12, 13, 14}
}

class ChannelAnalyzer:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
    
    def occupancy(self, window_seconds=60):
        now = int(time.time())
        rows = self.db.query(
            "SELECT channel, COUNT(*) as c FROM networks WHERE last_seen > ? AND channel IS NOT NULL GROUP BY channel",
            (now - window_seconds,)
        )
        return {r['channel']: r['c'] for r in rows}
    
    def get_channel_stats(self):
        rows = self.db.query(
            "SELECT channel, COUNT(*) as count, AVG(rssi) as avg_rssi FROM networks WHERE channel IS NOT NULL GROUP BY channel"
        )
        return [dict(r) for r in rows]
    
    def is_dfs_channel(self, channel):
        return channel in DFS_CHANNELS_5GHZ
    
    def get_overlapping_channels(self, channel):
        if 1 <= channel <= 14:
            return CHANNEL_OVERLAP_24.get(channel, {channel})
        elif channel > 14:
            return {channel - 2, channel - 1, channel, channel + 1, channel + 2}
        return {channel}
    
    def calculate_overlap_matrix(self, window_seconds=60):
        now = int(time.time())
        rows = self.db.query(
            """
            SELECT channel, COUNT(*) as count, AVG(rssi) as avg_rssi 
            FROM networks 
            WHERE last_seen > ? AND channel IS NOT NULL 
            GROUP BY channel
            """,
            (now - window_seconds,)
        )
        
        matrix = {}
        channel_data = {r['channel']: {'count': r['count'], 'avg_rssi': r['avg_rssi']} for r in rows}
        
        for channel, data in channel_data.items():
            overlapping = self.get_overlapping_channels(channel)
            interference = {}
            
            for overlap_ch in overlapping:
                if overlap_ch in channel_data and overlap_ch != channel:
                    interference[overlap_ch] = {
                        'networks': channel_data[overlap_ch]['count'],
                        'avg_rssi': channel_data[overlap_ch]['avg_rssi'],
                        'interference_score': channel_data[overlap_ch]['count'] * (channel_data[overlap_ch]['avg_rssi'] or -90) / 100
                    }
            
            matrix[channel] = {
                'networks': data['count'],
                'avg_rssi': data['avg_rssi'],
                'overlapping': interference,
                'is_dfs': self.is_dfs_channel(channel)
            }
        
        return matrix
    
    def get_best_channels(self, band='2.4GHz', max_interference=5):
        matrix = self.calculate_overlap_matrix()
        
        if band == '2.4GHz':
            channels = [ch for ch in range(1, 15) if ch in matrix]
        else:
            channels = [ch for ch in matrix.keys() if ch > 14]
        
        best_channels = []
        for ch in channels:
            if ch in matrix:
                total_interference = sum(
                    overlap['interference_score'] 
                    for overlap in matrix[ch]['overlapping'].values()
                )
                if total_interference <= max_interference:
                    best_channels.append({
                        'channel': ch,
                        'networks': matrix[ch]['networks'],
                        'interference': round(total_interference, 2),
                        'is_dfs': matrix[ch]['is_dfs']
                    })
        
        return sorted(best_channels, key=lambda x: (x['interference'], x['networks']))
