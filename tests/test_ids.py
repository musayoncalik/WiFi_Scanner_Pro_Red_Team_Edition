import pytest
import time
from utils.db import Database
from core.ids_engine import IDSEngine
import configparser


def test_ids_engine_instantiation():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('ids')
    cfg.set('ids', 'deauth_threshold', '50')
    cfg.set('ids', 'probe_threshold', '200')
    cfg.set('ids', 'beacon_threshold', '100')
    cfg.set('ids', 'poll_interval', '2')
    cfg.set('ids', 'window_seconds', '10')
    
    ids = IDSEngine(db=db, config=cfg)
    assert ids is not None
    assert ids.db == db
    assert ids.poll_interval == 2
    assert ids.window_seconds == 10


def test_ids_deauth_flood_detection():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('ids')
    cfg.set('ids', 'deauth_threshold', '5')
    cfg.set('ids', 'window_seconds', '10')
    cfg.set('ids', 'poll_interval', '1')
    
    ids = IDSEngine(db=db, config=cfg)
    
    now = int(time.time())
    for i in range(10):
        db.execute(
            "INSERT INTO frames (ts, type, subtype, src, dst, bssid, rssi) VALUES (?,?,?,?,?,?,?)",
            (now - i, '0', '12', 'aa:bb:cc:dd:ee:ff', 'ff:ee:dd:cc:bb:aa', '11:22:33:44:55:66', -50)
        )
    
    ids.check_deauth_flood()
    
    events = db.query("SELECT * FROM ids_events WHERE event_type = 'deauth_flood'")
    assert len(events) > 0


def test_ids_probe_storm_detection():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('ids')
    cfg.set('ids', 'probe_threshold', '10')
    cfg.set('ids', 'window_seconds', '10')
    
    ids = IDSEngine(db=db, config=cfg)
    
    now = int(time.time())
    for i in range(15):
        db.execute(
            "INSERT INTO frames (ts, type, subtype, src, dst, bssid, rssi) VALUES (?,?,?,?,?,?,?)",
            (now - i, '0', '4', 'aa:bb:cc:dd:ee:ff', 'ff:ff:ff:ff:ff:ff', None, -60)
        )
    
    ids.check_probe_storm()
    events = db.query("SELECT * FROM ids_events WHERE event_type = 'probe_storm'")
    assert len(events) > 0


def test_ids_beacon_flood_detection():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('ids')
    cfg.set('ids', 'beacon_threshold', '10')
    cfg.set('ids', 'window_seconds', '10')
    
    ids = IDSEngine(db=db, config=cfg)
    
    now = int(time.time())
    for i in range(15):
        db.execute(
            "INSERT INTO frames (ts, type, subtype, src, dst, bssid, rssi) VALUES (?,?,?,?,?,?,?)",
            (now - i, '0', '8', 'aa:bb:cc:dd:ee:ff', 'ff:ff:ff:ff:ff:ff', '11:22:33:44:55:66', -50)
        )
    
    ids.check_beacon_flood()
    events = db.query("SELECT * FROM ids_events WHERE event_type = 'beacon_flood'")
    assert len(events) > 0
