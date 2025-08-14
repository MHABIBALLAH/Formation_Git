from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.api.extensions import db
from src.core.vat.models import VatRecord
import datetime

vat = Blueprint('vat', __name__)

@vat.route('/reports', methods=['GET'])
@login_required
def get_vat_reports():
    """
    Returns a list of VAT records for the current user,
    optionally filtered by a date range.
    """
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    query = VatRecord.query.filter_by(user_id=current_user.id)

    if start_date_str:
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(VatRecord.period_start_date >= start_date)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD.'}), 400

    if end_date_str:
        try:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(VatRecord.period_end_date <= end_date)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD.'}), 400

    records = query.order_by(VatRecord.period_start_date.desc()).all()

    output = []
    for record in records:
        record_data = {
            'id': record.id,
            'period_key': record.period_key,
            'period_start_date': record.period_start_date.strftime('%Y-%m-%d'),
            'period_end_date': record.period_end_date.strftime('%Y-%m-%d'),
            'total_collected_vat': str(record.total_collected_vat),
            'total_deductible_vat': str(record.total_deductible_vat),
            'vat_due': str(record.vat_due),
            'status': record.status
        }
        output.append(record_data)

    return jsonify(output)
