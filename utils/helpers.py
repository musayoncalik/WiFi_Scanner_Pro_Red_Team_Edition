import math
import time

def db_now():
    return int(time.time())

def rssi_to_distance(rssi, freq_mhz=2400, tx_power=20):
    if rssi is None:
        return None
    
    try:
        fspl = tx_power - rssi
        exp = (fspl - 20 * math.log10(freq_mhz) - 32.44) / 20.0
        distance = 10 ** exp
        return round(distance, 2)
    except (ValueError, OverflowError):
        return None

def smooth(values, alpha=0.3):
    if not values:
        return []
    
    out = [values[0]]
    for v in values[1:]:
        smoothed = alpha * v + (1 - alpha) * out[-1]
        out.append(smoothed)
    return out

def format_mac(mac):
    if not mac:
        return None
    mac_clean = mac.replace(":", "").replace("-", "").upper()
    if len(mac_clean) != 12:
        return mac
    return ":".join([mac_clean[i:i+2] for i in range(0, 12, 2)])

def calculate_channel_overlap(ch1, ch2):
    if 1 <= ch1 <= 14 and 1 <= ch2 <= 14:
        overlap_24 = {
            1: {1, 2, 3, 4, 5},
            2: {1, 2, 3, 4, 5, 6},
            3: {1, 2, 3, 4, 5, 6, 7},
            4: {1, 2, 3, 4, 5, 6, 7, 8},
            5: {1, 2, 3, 4, 5, 6, 7, 8, 9},
            6: {2, 3, 4, 5, 6, 7, 8, 9, 10},
            7: {3, 4, 5, 6, 7, 8, 9, 10, 11},
            8: {4, 5, 6, 7, 8, 9, 10, 11},
            9: {5, 6, 7, 8, 9, 10, 11},
            10: {6, 7, 8, 9, 10, 11},
            11: {7, 8, 9, 10, 11},
            12: {8, 9, 10, 11, 12, 13},
            13: {9, 10, 11, 12, 13, 14},
            14: {10, 11, 12, 13, 14}
        }
        return ch2 in overlap_24.get(ch1, {ch1})
    elif ch1 > 14 and ch2 > 14:
        return abs(ch1 - ch2) <= 2
    return False
