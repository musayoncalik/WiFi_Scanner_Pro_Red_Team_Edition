from typing import Dict, Type, Any
from core.interfaces import IAnalyzer, IDetector
from core.channel_analyzer import ChannelAnalyzer
from core.health_analyzer import HealthAnalyzer
from core.snr_analyzer import SNRAnalyzer
from core.security_analyzer import SecurityAnalyzer
from core.rogue_ap_detector import RogueAPDetector
from core.ids_engine import IDSEngine
from utils.db import Database
from utils.config_manager import ConfigManager

class AnalyzerFactory:
    _analyzers: Dict[str, Type[Any]] = {
        'channel': ChannelAnalyzer,
        'health': HealthAnalyzer,
        'snr': SNRAnalyzer,
        'security': SecurityAnalyzer,
    }
    
    @classmethod
    def create(cls, analyzer_type: str, db: Database, config: ConfigManager) -> Any:
        if analyzer_type not in cls._analyzers:
            raise ValueError(f"Unknown analyzer type: {analyzer_type}")
        return cls._analyzers[analyzer_type](db, config)
    
    @classmethod
    def register(cls, analyzer_type: str, analyzer_class: Type[Any]) -> None:
        cls._analyzers[analyzer_type] = analyzer_class

class DetectorFactory:
    _detectors: Dict[str, Type[Any]] = {
        'rogue_ap': RogueAPDetector,
        'ids': IDSEngine,
    }
    
    @classmethod
    def create(cls, detector_type: str, db: Database, config: ConfigManager) -> Any:
        if detector_type not in cls._detectors:
            raise ValueError(f"Unknown detector type: {detector_type}")
        return cls._detectors[detector_type](db, config)
    
    @classmethod
    def register(cls, detector_type: str, detector_class: Type[Any]) -> None:
        cls._detectors[detector_type] = detector_class

