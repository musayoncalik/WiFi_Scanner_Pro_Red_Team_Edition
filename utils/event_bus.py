from typing import Dict, List, Callable, Any
from core.interfaces import IEventPublisher
import logging
import threading

log = logging.getLogger(__name__)

class EventBus(IEventPublisher):
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            if handler not in self._subscribers[event_type]:
                self._subscribers[event_type].append(handler)
                log.debug("Event handler subscribed: %s -> %s", event_type, handler.__name__)
    
    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        with self._lock:
            if event_type in self._subscribers:
                if handler in self._subscribers[event_type]:
                    self._subscribers[event_type].remove(handler)
                    log.debug("Event handler unsubscribed: %s -> %s", event_type, handler.__name__)
    
    def publish(self, event_type: str, data: Any) -> None:
        handlers = []
        with self._lock:
            if event_type in self._subscribers:
                handlers = self._subscribers[event_type].copy()
        
        for handler in handlers:
            try:
                handler(event_type, data)
            except Exception as e:
                log.exception("Event handler error: %s -> %s", event_type, e)
    
    def clear(self) -> None:
        with self._lock:
            self._subscribers.clear()

