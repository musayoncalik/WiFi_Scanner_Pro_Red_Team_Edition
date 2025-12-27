import logging

log = logging.getLogger(__name__)

class DeviceClassifier:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
        log.info("DeviceClassifier başlatıldı (placeholder)")
    
    def classify(self, mac, features):
        return "Unknown"
