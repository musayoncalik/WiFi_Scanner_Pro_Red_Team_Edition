import pytest
import tkinter as tk
from utils.db import Database
from gui.gui_main import WifiGuiApp
import configparser


def test_gui_init():
    db = Database(':memory:')
    db.migrate()
    
    class DummyScanner:
        def __init__(self):
            self.iface = 'wlan0mon'
            self.channel_hop = True
            self.channels = [1, 6, 11]
    
    class DummyIDS:
        pass
    
    cfg = configparser.ConfigParser()
    cfg.add_section('gui')
    cfg.set('gui', 'refresh_interval_ms', '2000')
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = WifiGuiApp(db=db, scanner=DummyScanner(), ids=DummyIDS(), config=cfg)
        assert app is not None
        assert app.db == db
        assert app.filter is not None
    finally:
        root.destroy()


def test_network_filter():
    from gui.gui_main import NetworkFilter
    
    filter_obj = NetworkFilter()
    filter_obj.vendor_filter = 'Apple'
    filter_obj.band_filter = '2.4GHz'
    filter_obj.security_filter = 'WPA2'
    filter_obj.rssi_min = -70
    filter_obj.rssi_max = -50
    
    networks = [
        {'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': 'Test', 'channel': 6, 'crypto': 'WPA2', 'rssi': -60, 'vendor': 'Apple'},
        {'bssid': '11:22:33:44:55:66', 'ssid': 'Test2', 'channel': 36, 'crypto': 'Open', 'rssi': -80, 'vendor': 'Samsung'}
    ]
    
    filtered = filter_obj.apply(networks)
    assert len(filtered) == 1
    assert filtered[0]['bssid'] == 'aa:bb:cc:dd:ee:ff'
