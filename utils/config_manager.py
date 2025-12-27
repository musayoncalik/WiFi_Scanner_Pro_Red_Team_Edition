import configparser
import os
from typing import Any, Optional, Dict
from core.interfaces import IConfigManager

class ConfigManager(IConfigManager):
    def __init__(self, config_path: str = "config.ini"):
        self.config_path = config_path
        self._config = configparser.ConfigParser()
        self._load()
    
    def _load(self) -> None:
        if os.path.exists(self.config_path):
            self._config.read(self.config_path)
        else:
            self._create_default()
    
    def _create_default(self) -> None:
        self._config['database'] = {'path': 'data/wifi_scanner.db'}
        self._config['logging'] = {
            'level': 'INFO',
            'file': 'data/logs/wifi_scanner.log',
            'max_bytes': '10485760',
            'backup_count': '3'
        }
        self._config['scanner'] = {
            'interface': 'wlan0',
            'monitor_interface': 'wlan0mon',
            'channel_hop': 'True',
            'channels': '1,6,11',
            'hop_interval': '5',
            'sniff_timeout': '2'
        }
        self._config['ids'] = {
            'deauth_threshold': '50',
            'probe_threshold': '200',
            'beacon_threshold': '100',
            'association_threshold': '100',
            'poll_interval': '2',
            'window_seconds': '10'
        }
        self._save()
    
    def _save(self) -> None:
        config_dir = os.path.dirname(self.config_path)
        if config_dir:
            os.makedirs(config_dir, exist_ok=True)
        with open(self.config_path, 'w') as f:
            self._config.write(f)
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        try:
            return self._config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        try:
            return self._config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        try:
            return self._config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def getfloat(self, section: str, key: str, fallback: float = 0.0) -> float:
        try:
            return self._config.getfloat(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def set(self, section: str, key: str, value: Any) -> None:
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, key, str(value))
        self._save()
    
    def get_section(self, section: str) -> Optional[Dict[str, str]]:
        if self._config.has_section(section):
            return dict(self._config.items(section))
        return None

