import os
import sys
import io
from flask import Flask, jsonify, send_from_directory, make_response

# Add the project root to the Python path to allow imports from `src`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.core.ocr.extractor import extract_invoice_data
from src.core.ocr.reader import extract_text_from_image
from src.core.reporting.summaries import generate_financial_summary
from src.core.accounting.journal import generate_entries_from_invoice
from src.core.export.fec_exporter import export_to_fec


# Define paths relative to the location of this app.py file
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(SRC_DIR, '..', 'web')
DATA_DIR = os.path.join(SRC_DIR, '..', '..', 'data', 'invoices')

app = Flask(__name__, static_folder=WEB_DIR, static_url_path='')

@app.route('/')
def serve_dashboard():
    """Serves the main dashboard page (index.html)."""
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/api/summary')
def get_financial_summary():
    """
    Processes a sample invoice and returns a financial summary.
    """
    try:
        invoice_path = os.path.join(DATA_DIR, 'synthetic_invoice.png')
        if not os.path.exists(invoice_path):
            return jsonify({"error": "Sample invoice not found."}), 404

        raw_text = extract_text_from_image(invoice_path)
        invoice_data = extract_invoice_data(raw_text)
        summary_data = generate_financial_summary([invoice_data])

        return jsonify(summary_data)
    except Exception as e:
        return jsonify({"error": "An internal error occurred.", "details": str(e)}), 500

@app.route('/api/export/fec')
def export_fec_file():
    """
    Generates and returns a FEC file for download based on a sample invoice.
    """
    try:
        # 1. Process the invoice to get accounting entries
        invoice_path = os.path.join(DATA_DIR, 'synthetic_invoice.png')
        if not os.path.exists(invoice_path):
            return jsonify({"error": "Sample invoice not found."}), 404

        raw_text = extract_text_from_image(invoice_path)
        invoice_data = extract_invoice_data(raw_text)
        entries = generate_entries_from_invoice(invoice_data)

        # 2. Export entries to FEC format
        fec_content = export_to_fec(entries)

        # 3. Create a response to trigger a file download
        response = make_response(fec_content)
        response.headers["Content-Disposition"] = "attachment; filename=fec.txt"
        response.headers["Content-Type"] = "text/plain; charset=utf-8"

        return response
    except Exception as e:
        return jsonify({"error": "An internal error occurred during FEC export.", "details": str(e)}), 500

@app.route('/api/health')
def health_check():
    """A simple health check endpoint to confirm the server is running."""
    return jsonify({"status": "ok"})
