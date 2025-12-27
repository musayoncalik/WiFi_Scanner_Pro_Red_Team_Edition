from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Callable

class IAnalyzer(ABC):
    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        pass

class IDetector(ABC):
    @abstractmethod
    def detect(self, data: Any) -> List[Dict[str, Any]]:
        pass

class IRepository(ABC):
    @abstractmethod
    def save(self, entity: Any) -> bool:
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Any]:
        pass

class IConfigManager(ABC):
    @abstractmethod
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        pass
    
    @abstractmethod
    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        pass
    
    @abstractmethod
    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        pass

class IEventPublisher(ABC):
    @abstractmethod
    def subscribe(self, event_type: str, handler: Callable) -> None:
        pass
    
    @abstractmethod
    def publish(self, event_type: str, data: Any) -> None:
        pass

