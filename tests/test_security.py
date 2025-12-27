import pytest
from utils.db import Database
from core.security_analyzer import SecurityAnalyzer
import configparser


def test_security_analyzer_basic():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('security')
    
    sa = SecurityAnalyzer(db=db, config=cfg)
    assert sa is not None
    assert sa.db == db
    assert sa.config == cfg


def test_security_analyzer_ies_extraction():
    db = Database(':memory:')
    db.migrate()
    cfg = configparser.ConfigParser()
    cfg.add_section('security')
    
    sa = SecurityAnalyzer(db=db, config=cfg)
    assert sa._extract_ies is not None
