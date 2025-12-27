from utils.db import Database
from reports.pdf_report import PDFReport
from reports.html_report import HTMLReport
from reports.csv_export import CSVExport

def run():
    db = Database(':memory:')
    db.migrate()
    db.execute("INSERT INTO networks (bssid, ssid, channel, rssi, last_seen) VALUES (?,?,?,?,?)",
               ('00:11:22:33:44:55','TEST_NET',6,-45, 0))
    pdf = PDFReport(db, output_dir='reports/output')
    p = pdf.generate_summary()
    html = HTMLReport(db, output_dir='reports/output')
    h = html.generate_summary()
    csv = CSVExport(db, output_dir='reports/output')
    c = csv.export_networks()
    print("Selftest generated:", p, h, c)

if __name__ == "__main__":
    run()
