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

@invoicing.route('/<int:invoice_id>/validate', methods=['POST'])
@login_required
def validate_invoice(invoice_id):
    """
    Validates an invoice and creates the corresponding financial transaction.
    """
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()

    if invoice.status != 'completed':
        return jsonify({'error': 'Only invoices with status "completed" can be validated.'}), 400

    if not invoice.total_ttc or not invoice.invoice_date:
        return jsonify({'error': 'Invoice is missing data required for transaction creation (date or total).'}), 400

    from src.core.cashflow.models import Transaction
    from src.core.vat.models import VatRecord

    # For a sales invoice, this would be a credit. For a bill, a debit.
    # We'll assume these are bills/expenses for now, so VAT is deductible.
    transaction = Transaction(
        description=f"Dépense pour facture #{invoice.id} - {invoice.supplier}",
        transaction_type='debit',
        amount=invoice.total_ttc * -1,
        transaction_date=invoice.invoice_date,
        user_id=current_user.id,
        invoice_id=invoice.id
    )

    # --- VAT Record Logic ---
    if invoice.total_vat and invoice.total_vat > 0:
        period_key = invoice.invoice_date.strftime('%Y-%m')
        # Find or create the VatRecord for the period
        vat_record = VatRecord.query.filter_by(user_id=current_user.id, period_key=period_key).first()
        if not vat_record:
            # Get the first and last day of the month
            start_of_month = invoice.invoice_date.replace(day=1)
            next_month = start_of_month.replace(day=28) + datetime.timedelta(days=4)
            end_of_month = next_month - datetime.timedelta(days=next_month.day)
            vat_record = VatRecord(
                user_id=current_user.id,
                period_key=period_key,
                period_start_date=start_of_month,
                period_end_date=end_of_month,
                total_collected_vat=0,
                total_deductible_vat=0
            )
            db.session.add(vat_record)

        # Add the invoice's VAT to the deductible total
        vat_record.total_deductible_vat += invoice.total_vat
        # Recalculate VAT due
        vat_record.vat_due = vat_record.total_collected_vat - vat_record.total_deductible_vat

    invoice.status = 'validated'

    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': f'Invoice {invoice.id} validated and transaction created.'}), 200

@invoicing.route('', methods=['GET'])
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
            invoice.invoice_date = datetime.datetime.strptime(extracted_data.get('date'), '%d/%m/%Y').date() if extracted_data.get('date') else None
            invoice.total_ht = extracted_data.get('total_ht')
            invoice.total_ttc = extracted_data.get('total_ttc')
            invoice.total_vat = extracted_data.get('vat_amount') # Correct key from extractor
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
            import logging
            logging.basicConfig(level=logging.INFO)
            logging.info(f"Error processing invoice: {e}")
            logging.info(f"Raw text: {raw_text}")
            logging.info(f"Extracted data: {extracted_data}")
            # In a real app, log the error `e`
            return jsonify({'error': 'Failed to process invoice', 'details': str(e)}), 500

    return jsonify({'error': 'File type not allowed'}), 400
