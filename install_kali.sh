#!/usr/bin/env bash
# WiFi Scanner Pro - All-in-One Yönetim Aracı
# Kurulum, Test, Ayar ve Başlatma işlemlerini tek dosyada toplar.

set -e

# --- RENKLER ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# --- KONTROLLER ---
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[HATA] Bu araç root yetkisi gerektirir.${NC}"
    echo "Lütfen sudo ile çalıştırın: sudo ./setup_tool.sh"
    exit 1
fi

# --- FONKSİYONLAR ---

function print_header() {
    clear
    echo -e "${BLUE}======================================================${NC}"
    echo -e "${BLUE}    WiFi Scanner Pro - Yönetim Paneli v2.0            ${NC}"
    echo -e "${BLUE}======================================================${NC}"
    echo
}

function install_environment() {
    print_header
    echo -e "${YELLOW}[*] Sistem paketleri güncelleniyor...${NC}"
    apt update -qq
    
    echo -e "${YELLOW}[*] Gerekli sistem araçları kuruluyor (APT)...${NC}"
    apt install -y python3-full python3-pip python3-venv python3-tk build-essential \
        libpcap-dev libssl-dev aircrack-ng iw wireless-tools net-tools tcpdump git pciutils \
        wget

    echo -e "${YELLOW}[*] Python Sanal Ortamı (venv) hazırlanıyor...${NC}"
    if [ -d "venv" ]; then
        echo -e "${CYAN}   -> Mevcut venv klasörü bulundu, güncelleniyor...${NC}"
    else
        python3 -m venv venv
        echo -e "${GREEN}   -> Yeni venv klasörü oluşturuldu.${NC}"
    fi

    echo -e "${YELLOW}[*] Python kütüphaneleri kuruluyor (PIP)...${NC}"
    # requirements.txt dosyasına ihtiyaç duymadan direkt kuruyoruz
    ./venv/bin/pip install --upgrade pip setuptools wheel
    ./venv/bin/pip install scapy manuf reportlab jinja2 colorama matplotlib pandas numpy pillow

    echo -e "${YELLOW}[*] Klasör yapısı ve izinler ayarlanıyor...${NC}"
    mkdir -p data reports/output logs
    chmod -R 777 data/ reports/ logs/
    
    # Manuf dosyasını indir
    if [ ! -f "data/manuf" ]; then
        echo -e "${YELLOW}[*] MAC adres veritabanı indiriliyor...${NC}"
        wget -q https://gitlab.com/wireshark/wireshark/-/raw/master/manuf -O data/manuf || true
    fi

    echo
    echo -e "${GREEN}✅ KURULUM TAMAMLANDI!${NC}"
    read -p "Menüye dönmek için Enter'a basın..."
}

function enable_monitor_mode() {
    print_header
    echo -e "${YELLOW}[*] Ağ kartları taranıyor...${NC}"
    iw dev
    echo
    echo -e "${CYAN}Lütfen kullanılacak kartın ismini yazın (örn: wlan0):${NC}"
    read iface

    if [ -z "$iface" ]; then
        echo -e "${RED}İsim boş olamaz!${NC}"
        sleep 2
        return
    fi

    echo -e "${YELLOW}[*] Çakışan servisler durduruluyor...${NC}"
    airmon-ng check kill

    echo -e "${YELLOW}[*] $iface monitor moduna alınıyor...${NC}"
    airmon-ng start $iface

    echo
    echo -e "${GREEN}✅ İşlem tamamlandı. Lütfen iwconfig ile kontrol edin.${NC}"
    read -p "Devam etmek için Enter..."
}

function run_diagnostics() {
    print_header
    echo -e "${YELLOW}[*] Tanı testi başlatılıyor...${NC}"
    
    # 1. Kart Kontrolü
    monitor_iface=$(iwconfig 2>/dev/null | grep "Mode:Monitor" | awk '{print $1}')
    
    if [ -z "$monitor_iface" ]; then
        echo -e "${RED}[X] HATA: Monitor modunda kart bulunamadı!${NC}"
        echo "Lütfen ana menüden '2. Monitor Modu Aç' seçeneğini kullanın."
    else
        echo -e "${GREEN}[OK] Monitor modunda kart bulundu: $monitor_iface${NC}"
        
        # 2. Paket Yakalama Testi
        echo -e "${YELLOW}[*] $monitor_iface üzerinde 5 saniyelik paket yakalama testi yapılıyor...${NC}"
        packet_count=$(timeout 5 tcpdump -i $monitor_iface -c 10 2>/dev/null | wc -l)
        
        if [ $packet_count -gt 0 ]; then
             echo -e "${GREEN}[OK] BAŞARILI! $packet_count paket yakalandı.${NC}"
             echo -e "${GREEN}Sistem çalışmaya hazır.${NC}"
        else
             echo -e "${RED}[X] HATA: Kart monitor modunda ama paket yakalamıyor.${NC}"
             echo "Sanal makine kullanıyorsanız USB adaptörün bağlı olduğundan emin olun."
        fi
    fi
    echo
    read -p "Menüye dönmek için Enter..."
}

function reset_db() {
    print_header
    echo -e "${RED}!!! DİKKAT !!!${NC}"
    echo "Mevcut veritabanı (data/wifi_scanner.db) silinecek."
    read -p "Emin misiniz? (e/h): " choice
    if [[ "$choice" == "e" || "$choice" == "E" ]]; then
        rm -f data/wifi_scanner.db
        echo -e "${GREEN}Veritabanı silindi. Program başlatılınca yeniden oluşacak.${NC}"
    else
        echo "İptal edildi."
    fi
    sleep 2
}

function start_app() {
    print_header
    if [ ! -d "venv" ]; then
        echo -e "${RED}[HATA] Sanal ortam bulunamadı! Önce kurulum yapın (Seçenek 1).${NC}"
        read -p "Enter..."
        return
    fi

    if [ ! -f "main.py" ]; then
        echo -e "${RED}[HATA] main.py dosyası bulunamadı!${NC}"
        read -p "Enter..."
        return
    fi

    echo -e "${GREEN}🚀 Uygulama Başlatılıyor...${NC}"
    echo "Durdurmak için GUI penceresini kapatın veya CTRL+C yapın."
    echo "--------------------------------------------------------"
    
    # Sanal ortam python'u ile başlat
    sudo -E ./venv/bin/python3 main.py
    
    echo
    read -p "Uygulama kapandı. Menüye dönmek için Enter..."
}

# --- ANA DÖNGÜ ---

while true; do
    print_header
    echo "1) 📦 Kurulumu Yap / Güncelle (Sanal Ortam)"
    echo "2) 📡 Monitor Modu Aç (airmon-ng)"
    echo "3) 🩺 Sistem Testi (Diagnostik)"
    echo "4) 🧹 Veritabanını Tamamen Sil (Hard Reset)"
    echo "5) 🚀 UYGULAMAYI BAŞLAT"
    echo "6) ❌ Çıkış"
    echo
    read -p "Seçiminiz (1-6): " opt

    case $opt in
        1) install_environment ;;
        2) enable_monitor_mode ;;
        3) run_diagnostics ;;
        4) reset_db ;;
        5) start_app ;;
        6) echo "Güle güle!"; exit 0 ;;
        *) echo "Geçersiz seçim."; sleep 1 ;;
    esac
done