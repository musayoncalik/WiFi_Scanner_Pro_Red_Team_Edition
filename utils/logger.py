import logging
import logging.handlers
import os

def setup_logging(level='INFO', logfile='data/logs/wifi_scanner.log',
                  max_bytes=10*1024*1024, backup_count=3):
    log_dir = os.path.dirname(logfile)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    
    fh = logging.handlers.RotatingFileHandler(
        logfile,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    
    return logging.getLogger(__name__)
