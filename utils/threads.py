import threading
import logging
import time

log = logging.getLogger(__name__)

class ThreadManager:
    
    def __init__(self):
        self.threads = {}
        self.stop_events = {}
        self._lock = threading.Lock()
    
    def start_background(self, name, target, args=()):
        with self._lock:
            if name in self.threads:
                log.warning("Thread zaten çalışıyor: %s", name)
                return self.threads[name]
            
            stop_event = threading.Event()
            
            def wrapper():
                try:
                    target(stop_event, *args)
                except TypeError:
                    try:
                        target(*args)
                    except Exception as e:
                        log.exception("Thread %s hatası: %s", name, e)
                except Exception as e:
                    log.exception("Thread %s çöktü: %s", name, e)
            
            t = threading.Thread(target=wrapper, name=name, daemon=True)
            self.threads[name] = t
            self.stop_events[name] = stop_event
            t.start()
            log.info("Thread başlatıldı: %s", name)
            return t
    
    def stop_all(self, timeout=5):
        with self._lock:
            for name, ev in self.stop_events.items():
                ev.set()
                log.debug("Stop event set edildi: %s", name)
            
            for name, t in self.threads.items():
                t.join(timeout)
                if t.is_alive():
                    log.warning("Thread zaman aşımı: %s", name)
                else:
                    log.info("Thread durduruldu: %s", name)
            
            self.threads.clear()
            self.stop_events.clear()
    
    def stop_thread(self, name, timeout=5):
        with self._lock:
            if name in self.stop_events:
                self.stop_events[name].set()
            if name in self.threads:
                self.threads[name].join(timeout)
                if not self.threads[name].is_alive():
                    del self.threads[name]
                    del self.stop_events[name]
                    log.info("Thread durduruldu: %s", name)
