#!/usr/bin/env bash
# WiFi Scanner CLI Menu - Zenity

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR" || exit 1

CHOICE=$(zenity --list \
    --title="WiFi Scanner CLI" \
    --text="Bir işlem seçin:" \
    --radiolist \
    --column="" \
    --column="İşlem" \
    TRUE "GUI Başlat" \
    FALSE "PDF Rapor Oluştur" \
    FALSE "HTML Rapor Oluştur" \
    FALSE "CSV Dışa Aktar" \
    --width=400 \
    --height=250)

if [ -z "$CHOICE" ]; then
    exit 0
fi

case "$CHOICE" in
    "GUI Başlat")
        if [ "$EUID" -ne 0 ]; then
            zenity --error --text="GUI başlatmak için root yetkisi gereklidir.\n\nLütfen sudo ile çalıştırın:\nsudo ./cli/zenity_menu.sh"
        else
            python3 main.py
        fi
        ;;
    "PDF Rapor Oluştur")
        OUTPUT=$(python3 -c "
from utils.db import Database
from reports.pdf_report import PDFReport
import sys
try:
    db = Database()
    db.migrate()
    report = PDFReport(db)
    path = report.generate_summary()
    print(f'PDF raporu oluşturuldu:\n{path}')
except Exception as e:
    print(f'Hata: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)
        if [ $? -eq 0 ]; then
            zenity --info --title="Başarılı" --text="$OUTPUT"
        else
            zenity --error --title="Hata" --text="$OUTPUT"
        fi
        ;;
    "HTML Rapor Oluştur")
        OUTPUT=$(python3 -c "
from utils.db import Database
from reports.html_report import HTMLReport
import sys
try:
    db = Database()
    db.migrate()
    report = HTMLReport(db)
    path = report.generate_summary()
    print(f'HTML raporu oluşturuldu:\n{path}')
except Exception as e:
    print(f'Hata: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)
        if [ $? -eq 0 ]; then
            zenity --info --title="Başarılı" --text="$OUTPUT"
        else
            zenity --error --title="Hata" --text="$OUTPUT"
        fi
        ;;
    "CSV Dışa Aktar")
        OUTPUT=$(python3 -c "
from utils.db import Database
from reports.csv_export import CSVExport
import sys
try:
    db = Database()
    db.migrate()
    export = CSVExport(db)
    path = export.export_networks()
    print(f'CSV dosyası oluşturuldu:\n{path}')
except Exception as e:
    print(f'Hata: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)
        if [ $? -eq 0 ]; then
            zenity --info --title="Başarılı" --text="$OUTPUT"
        else
            zenity --error --title="Hata" --text="$OUTPUT"
        fi
        ;;
esac
