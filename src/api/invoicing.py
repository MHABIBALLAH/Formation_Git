import os
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from src.api.app import db
from src.core.invoicing.models import Invoice, LineItem
from src.core.ocr.reader import extract_text_from_image
from src.core.ocr.extractor import extract_invoice_data
import datetime

invoicing = Blueprint('invoicing', __name__)

# Define a folder to store uploaded invoices
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'instance', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@invoicing.route('/', methods=['GET'])
@login_required
def list_invoices():
    """Returns a list of invoices for the current user."""
    invoices = Invoice.query.filter_by(user_id=current_user.id).order_by(Invoice.created_at.desc()).all()

    output = []
    for invoice in invoices:
        invoice_data = {
            'id': invoice.id,
            'filename': invoice.filename,
            'status': invoice.status,
            'supplier': invoice.supplier,
            'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d') if invoice.invoice_date else None,
            'total_ttc': str(invoice.total_ttc) if invoice.total_ttc else '0.00', # Use str for decimal
            'created_at': invoice.created_at.isoformat()
        }
        output.append(invoice_data)

    return jsonify(output)

@invoicing.route('/upload', methods=['POST'])
@login_required
def upload_invoice():
    """Handles invoice file uploads and processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Ensure the upload folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 1. Create initial invoice record
        invoice = Invoice(
            filename=filename,
            user_id=current_user.id,
            status='processing'
        )
        db.session.add(invoice)
        db.session.commit()

        try:
            # 2. Process the file
            raw_text = extract_text_from_image(filepath) # Assuming this works for PDFs too if dependencies are present
            extracted_data = extract_invoice_data(raw_text)

            # 3. Update invoice with extracted data
            invoice.supplier = extracted_data.get('supplier')
            invoice.invoice_date = datetime.datetime.strptime(extracted_data.get('date'), '%Y-%m-%d').date() if extracted_data.get('date') else None
            invoice.total_ht = extracted_data.get('total_ht')
            invoice.total_ttc = extracted_data.get('total_ttc')
            invoice.total_vat = extracted_data.get('total_vat')
            invoice.status = 'completed'
            invoice.processed_at = datetime.datetime.utcnow()

            # 4. Create line items
            for item_data in extracted_data.get('line_items', []):
                line_item = LineItem(
                    description=item_data.get('description'),
                    quantity=item_data.get('quantity'),
                    unit_price_ht=item_data.get('unit_price'),
                    total_ht=item_data.get('total'),
                    invoice_id=invoice.id
                )
                db.session.add(line_item)

            db.session.commit()

            return jsonify({'message': 'Invoice processed successfully', 'invoice_id': invoice.id}), 201

        except Exception as e:
            # 5. Handle errors
            invoice.status = 'error'
            db.session.commit()
            # In a real app, log the error `e`
            return jsonify({'error': 'Failed to process invoice', 'details': str(e)}), 500

    return jsonify({'error': 'File type not allowed'}), 400
