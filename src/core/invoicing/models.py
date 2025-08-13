from sqlalchemy.orm import relationship
from src.api.extensions import db
import datetime

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='processing')

    # Extracted data
    supplier = db.Column(db.String(255), nullable=True)
    invoice_date = db.Column(db.Date, nullable=True)
    total_ht = db.Column(db.Numeric(10, 2), nullable=True)
    total_ttc = db.Column(db.Numeric(10, 2), nullable=True)
    total_vat = db.Column(db.Numeric(10, 2), nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=db.backref('invoices', lazy=True))
    line_items = relationship('LineItem', back_populates='invoice', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Invoice {self.id} ({self.filename})>'

class LineItem(db.Model):
    __tablename__ = 'line_items'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=True, default=1)
    unit_price_ht = db.Column(db.Numeric(10, 2), nullable=True)
    total_ht = db.Column(db.Numeric(10, 2), nullable=False)
    vat_rate = db.Column(db.Numeric(5, 2), nullable=True) # e.g., 20.00, 5.50
    vat_amount = db.Column(db.Numeric(10, 2), nullable=True)

    # Relationships
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    invoice = relationship('Invoice', back_populates='line_items')

    def __repr__(self):
        return f'<LineItem {self.id} ({self.description})>'
