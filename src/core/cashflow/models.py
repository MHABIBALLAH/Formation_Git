from sqlalchemy.orm import relationship
from src.api.extensions import db
import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    # 'credit' for inflows (revenue), 'debit' for outflows (expenses)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False, default=datetime.date.today)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=db.backref('transactions', lazy=True))

    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=True)
    invoice = relationship('Invoice', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f'<Transaction {self.id} ({self.transaction_type} {self.amount})>'
