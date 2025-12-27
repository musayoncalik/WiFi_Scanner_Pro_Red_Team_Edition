from abc import ABC, abstractmethod
from typing import List, Dict, Any
from core.interfaces import IAnalyzer

class AnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        pass

class ChannelAnalysisStrategy(AnalysisStrategy):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        channel = data.get('channel')
        if not channel:
            return {'status': 'error', 'message': 'Channel not provided'}
        
        occupancy = data.get('occupancy', {})
        overlap = data.get('overlap', {})
        
        return {
            'status': 'success',
            'channel': channel,
            'occupancy': occupancy.get(channel, 0),
            'overlap_count': len(overlap.get(channel, {}).get('overlapping', {})),
            'is_dfs': data.get('is_dfs', False)
        }

class SecurityAnalysisStrategy(AnalysisStrategy):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        crypto = data.get('crypto', 'Unknown')
        wps = data.get('wps', False)
        rsn = data.get('rsn', False)
        
        risk_score = 0.0
        if crypto == 'Open':
            risk_score = 1.0
        elif crypto == 'WPA':
            risk_score = 0.7
        elif crypto == 'WPA2':
            risk_score = 0.3
        elif crypto == 'WPA3':
            risk_score = 0.1
        
        if wps:
            risk_score += 0.2
        
        return {
            'status': 'success',
            'crypto': crypto,
            'wps_enabled': wps,
            'rsn_enabled': rsn,
            'risk_score': min(risk_score, 1.0),
            'recommendation': self._get_recommendation(risk_score)
        }
    
    def _get_recommendation(self, risk_score: float) -> str:
        if risk_score >= 0.8:
            return "Yüksek risk - Güvenlik protokolü değiştirilmeli"
        elif risk_score >= 0.5:
            return "Orta risk - Güvenlik iyileştirmeleri önerilir"
        else:
            return "Düşük risk - Güvenlik durumu iyi"

class StrategyContext:
    def __init__(self, strategy: AnalysisStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: AnalysisStrategy) -> None:
        self._strategy = strategy
    
    def execute(self, data: Any) -> Dict[str, Any]:
        return self._strategy.analyze(data)

