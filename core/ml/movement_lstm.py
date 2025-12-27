import logging

log = logging.getLogger(__name__)

class MovementLSTM:
    
    def __init__(self, db, config):
        self.db = db
        self.config = config
        log.info("MovementLSTM başlatıldı (placeholder)")
    
    def predict_movement(self, sequence):
        return None
