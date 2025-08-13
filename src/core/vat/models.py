from sqlalchemy.orm import relationship
from src.api.extensions import db
import datetime

class VatRecord(db.Model):
    __tablename__ = 'vat_records'

    id = db.Column(db.Integer, primary_key=True)

    # The period this record applies to
    period_key = db.Column(db.String(7), nullable=False) # e.g., "2025-01" for monthly
    period_start_date = db.Column(db.Date, nullable=False)
    period_end_date = db.Column(db.Date, nullable=False)

    # Aggregated amounts
    total_collected_vat = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    total_deductible_vat = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    vat_due = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)

    # Status
    status = db.Column(db.String(50), nullable=False, default='open') # open, declared

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=db.backref('vat_records', lazy=True))

    __table_args__ = (db.UniqueConstraint('user_id', 'period_key', name='_user_period_uc'),)

    def __repr__(self):
        return f'<VatRecord {self.period_key} (Due: {self.vat_due})>'
