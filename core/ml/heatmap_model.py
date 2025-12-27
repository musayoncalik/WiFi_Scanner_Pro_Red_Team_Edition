import logging

log = logging.getLogger(__name__)

class HeatmapModel:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
        log.info("HeatmapModel başlatıldı (placeholder)")
    
    def predict_heatmap(self, features):
        return {}
