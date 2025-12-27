import subprocess
import logging
import os
import time

log = logging.getLogger(__name__)

def check_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

def check_interface_exists(interface):
    try:
        result = subprocess.run(
            ['ip', 'link', 'show', interface],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False

def enable_monitor(interface, monitor_if=None):
    if not check_root():
        log.warning("Monitor mode için root yetkisi gerekli")
        return None
    
    if not check_interface_exists(interface):
        log.error("Interface bulunamadı: %s", interface)
        return None
    
    try:
        result = subprocess.run(
            ['which', 'airmon-ng'],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode == 0:
            log.info("airmon-ng kullanılarak monitor mode etkinleştiriliyor...")
            subprocess.run(['airmon-ng', 'check', 'kill'], check=False, timeout=10)
            time.sleep(1)
            
            cmd = ['airmon-ng', 'start', interface]
            if monitor_if:
                cmd.append(monitor_if)
            
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            if result.returncode == 0:
                monitor_name = monitor_if or f"{interface}mon"
                log.info("Monitor mode etkinleştirildi: %s", monitor_name)
                return monitor_name
        
        log.info("iw/ip kullanılarak monitor mode etkinleştiriliyor...")
        subprocess.run(
            ['ip', 'link', 'set', interface, 'down'],
            check=False,
            timeout=5
        )
        time.sleep(0.5)
        
        result = subprocess.run(
            ['iw', interface, 'set', 'type', 'monitor'],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode != 0:
            log.error("Monitor mode etkinleştirilemedi: %s", result.stderr.decode())
            return None
        
        subprocess.run(
            ['ip', 'link', 'set', interface, 'up'],
            check=False,
            timeout=5
        )
        time.sleep(0.5)
        
        log.info("Monitor mode etkinleştirildi: %s", interface)
        return interface
        
    except subprocess.TimeoutExpired:
        log.error("Monitor mode etkinleştirme zaman aşımı")
        return None
    except FileNotFoundError:
        log.error("Gerekli araçlar bulunamadı (iw, ip, airmon-ng)")
        return None
    except Exception as e:
        log.exception("Monitor mode etkinleştirme hatası: %s", e)
        return None

def disable_monitor(interface):
    if not check_root():
        log.warning("Monitor mode kapatma için root yetkisi gerekli")
        return False
    
    try:
        result = subprocess.run(
            ['which', 'airmon-ng'],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode == 0:
            subprocess.run(
                ['airmon-ng', 'stop', interface],
                check=False,
                timeout=10
            )
            log.info("Monitor mode kapatıldı (airmon-ng): %s", interface)
            return True
        
        subprocess.run(
            ['ip', 'link', 'set', interface, 'down'],
            check=False,
            timeout=5
        )
        time.sleep(0.5)
        
        subprocess.run(
            ['iw', interface, 'set', 'type', 'managed'],
            check=False,
            timeout=5
        )
        
        subprocess.run(
            ['ip', 'link', 'set', interface, 'up'],
            check=False,
            timeout=5
        )
        
        log.info("Monitor mode kapatıldı: %s", interface)
        return True
        
    except Exception as e:
        log.exception("Monitor mode kapatma hatası: %s", e)
        return False

def get_available_interfaces():
    try:
        result = subprocess.run(
            ['iw', 'dev'],
            capture_output=True,
            timeout=5,
            text=True
        )
        if result.returncode == 0:
            interfaces = []
            for line in result.stdout.split('\n'):
                if 'Interface' in line:
                    iface = line.split('Interface')[1].strip()
                    interfaces.append(iface)
            return interfaces
    except Exception:
        pass
    return []
