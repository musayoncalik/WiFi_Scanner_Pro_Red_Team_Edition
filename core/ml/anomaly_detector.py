import logging

log = logging.getLogger(__name__)

class AnomalyDetector:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
        log.info("AnomalyDetector başlatıldı (placeholder)")
    
    def detect(self, data):
        return []
