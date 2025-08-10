import os
from flask import Flask, jsonify, send_from_directory

# This is a bit of a hack to make sure we can import from the parent `src` directory.
# A better solution in a larger app would be a proper package installation (setup.py).
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.ocr.extractor import extract_invoice_data
from core.ocr.reader import extract_text_from_image
from core.reporting.summaries import generate_financial_summary

# Define paths relative to the location of this app.py file
# Assumes app.py is in src/api/
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
    In a real app, this would process multiple invoices, likely from a database.
    """
    try:
        # For this demonstration, we process one specific invoice to generate a summary.
        invoice_path = os.path.join(DATA_DIR, 'synthetic_invoice.png')

        if not os.path.exists(invoice_path):
            return jsonify({"error": "Sample invoice not found."}), 404

        raw_text = extract_text_from_image(invoice_path)
        invoice_data = extract_invoice_data(raw_text)

        # The summary function expects a list of invoices.
        summary_data = generate_financial_summary([invoice_data])

        return jsonify(summary_data)

    except Exception as e:
        # In a real app, you'd have more specific error handling and logging.
        return jsonify({"error": "An internal error occurred.", "details": str(e)}), 500

@app.route('/api/health')
def health_check():
    """A simple health check endpoint to confirm the server is running."""
    return jsonify({"status": "ok"})
