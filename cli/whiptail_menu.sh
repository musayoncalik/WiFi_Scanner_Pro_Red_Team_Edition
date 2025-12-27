#!/usr/bin/env bash
# WiFi Scanner CLI Menu - Whiptail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR" || exit 1

CHOICE=$(whiptail --title "WiFi Scanner CLI" \
    --menu "Bir işlem seçin:" 15 60 5 \
    "1" "GUI Başlat" \
    "2" "PDF Rapor Oluştur" \
    "3" "HTML Rapor Oluştur" \
    "4" "CSV Dışa Aktar" \
    "5" "Çıkış" \
    3>&1 1>&2 2>&3)

exitstatus=$?

if [ $exitstatus = 0 ]; then
    case $CHOICE in
        1)
            if [ "$EUID" -ne 0 ]; then
                whiptail --title "Hata" --msgbox "GUI başlatmak için root yetkisi gereklidir.\n\nLütfen sudo ile çalıştırın: sudo ./cli/whiptail_menu.sh" 10 60
            else
                python3 main.py
            fi
            ;;
        2)
            OUTPUT=$(python3 -c "
from utils.db import Database
from reports.pdf_report import PDFReport
import sys
try:
    db = Database()
    db.migrate()
    report = PDFReport(db)
    path = report.generate_summary()
    print(f'PDF raporu oluşturuldu: {path}')
except Exception as e:
    print(f'Hata: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)
            whiptail --title "PDF Rapor" --msgbox "$OUTPUT" 10 60
            ;;
        3)
            OUTPUT=$(python3 -c "
from utils.db import Database
from reports.html_report import HTMLReport
import sys
try:
    db = Database()
    db.migrate()
    report = HTMLReport(db)
    path = report.generate_summary()
    print(f'HTML raporu oluşturuldu: {path}')
except Exception as e:
    print(f'Hata: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)
            whiptail --title "HTML Rapor" --msgbox "$OUTPUT" 10 60
            ;;
        4)
            OUTPUT=$(python3 -c "
from utils.db import Database
from reports.csv_export import CSVExport
import sys
try:
    db = Database()
    db.migrate()
    export = CSVExport(db)
    path = export.export_networks()
    print(f'CSV dosyası oluşturuldu: {path}')
except Exception as e:
    print(f'Hata: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)
            whiptail --title "CSV Export" --msgbox "$OUTPUT" 10 60
            ;;
        5)
            exit 0
            ;;
    esac
fi
