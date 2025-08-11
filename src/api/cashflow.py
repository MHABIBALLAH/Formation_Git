from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.api.extensions import db
from src.core.cashflow.models import Transaction
from sqlalchemy import func
import datetime

cashflow = Blueprint('cashflow', __name__)

@cashflow.route('/', methods=['GET'])
@login_required
def get_cashflow_summary():
    """
    Calculates and returns a summary of cash flow based on transactions.
    Supports filtering by a date range.
    """
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Base query for the current user's transactions
    query = db.session.query(
        Transaction.transaction_type,
        func.sum(Transaction.amount).label('total')
    ).filter(Transaction.user_id == current_user.id)

    # Apply date filters if provided
    if start_date_str:
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Transaction.transaction_date >= start_date)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD.'}), 400

    if end_date_str:
        try:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Transaction.transaction_date <= end_date)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD.'}), 400

    # Group by transaction type to get separate totals for debit and credit
    results = query.group_by(Transaction.transaction_type).all()

    inflows = 0
    outflows = 0

    for r in results:
        if r.transaction_type == 'credit':
            # Amount is stored as positive
            inflows = float(r.total) if r.total is not None else 0
        elif r.transaction_type == 'debit':
            # Amount is stored as negative, so we take the absolute value for "outflows"
            outflows = abs(float(r.total)) if r.total is not None else 0

    net_balance = inflows - outflows

    summary = {
        'total_inflows': inflows,
        'total_outflows': outflows,
        'net_balance': net_balance
    }

    return jsonify(summary)
