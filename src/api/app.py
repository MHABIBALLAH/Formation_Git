import os
import sys
from flask import Flask, jsonify, send_from_directory, make_response

# --- Project Path Setup ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# --- Local Imports ---
from src.api.extensions import db, bcrypt, login_manager, migrate
from src.core.auth.models import User # Ensures user_loader is registered

def create_app(config_object='src.config.DevelopmentConfig'):
    """Application factory pattern."""
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web'),
                static_url_path='')

    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = 'info'

    @login_manager.unauthorized_handler
    def unauthorized():
        """Handle unauthorized requests for the API."""
        return jsonify({'error': 'Authentication required'}), 401

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints and routes within the app context
    with app.app_context():
        # Blueprints
        from src.api.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

        # Main application routes
        register_main_routes(app)

    return app

def register_main_routes(app):
    """Register the main application routes to avoid cluttering the factory."""
    from src.core.ocr.extractor import extract_invoice_data
    from src.core.ocr.reader import extract_text_from_image
    from src.core.reporting.summaries import generate_financial_summary
    from src.core.accounting.journal import generate_entries_from_invoice
    from src.core.export.fec_exporter import export_to_fec
    from flask_login import login_required

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    WEB_DIR = app.static_folder
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'invoices')

    @app.route('/')
    def serve_dashboard():
        return send_from_directory(WEB_DIR, 'index.html')

    @app.route('/api/summary')
    @login_required
    def get_financial_summary():
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
    @login_required
    def export_fec_file():
        try:
            invoice_path = os.path.join(DATA_DIR, 'synthetic_invoice.png')
            if not os.path.exists(invoice_path):
                return jsonify({"error": "Sample invoice not found."}), 404
            raw_text = extract_text_from_image(invoice_path)
            invoice_data = extract_invoice_data(raw_text)
            entries = generate_entries_from_invoice(invoice_data)
            fec_content = export_to_fec(entries)
            response = make_response(fec_content)
            response.headers["Content-Disposition"] = "attachment; filename=fec.txt"
            response.headers["Content-Type"] = "text/plain; charset=utf-8"
            return response
        except Exception as e:
            return jsonify({"error": "An internal error occurred during FEC export.", "details": str(e)}), 500

    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "ok"})
