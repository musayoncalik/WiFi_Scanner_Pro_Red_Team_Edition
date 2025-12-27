import pytest
import time
from utils.db import Database
from core.scanner import WifiScanner
import configparser


def test_db_migration():
    db = Database(':memory:')
    db.migrate()
    rows = db.query("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [r['name'] for r in rows]
    assert 'networks' in table_names
    assert 'frames' in table_names
    assert 'ids_events' in table_names
    assert 'clients' in table_names


def test_scanner_initialization():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('scanner')
    cfg.set('scanner', 'monitor_interface', 'wlan0mon')
    cfg.set('scanner', 'channel_hop', 'False')
    cfg.set('scanner', 'channels', '1,6,11')
    cfg.set('scanner', 'hop_interval', '5')
    cfg.set('scanner', 'sniff_timeout', '2')
    
    scanner = WifiScanner(db=db, config=cfg)
    assert scanner.db == db
    assert scanner.iface == 'wlan0mon'
    assert scanner.channel_hop is False
    assert scanner.channels == [1, 6, 11]


def test_scanner_channel_extraction():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('scanner')
    scanner = WifiScanner(db=db, config=cfg)
    
    assert scanner._extract_channel is not None


def test_scanner_crypto_extraction():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('scanner')
    scanner = WifiScanner(db=db, config=cfg)
    
    assert scanner._extract_crypto is not None
