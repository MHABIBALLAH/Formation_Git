from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class AccountingEntry:
    """
    Represents a single accounting entry (a line in a journal).
    Ensures that each entry has either a debit or a credit, but not both.
    """
    entry_date: date
    account_number: int
    account_name: str
    description: str
    debit: Optional[float] = None
    credit: Optional[float] = None

    def __post_init__(self):
        if self.debit is None and self.credit is None:
            raise ValueError("An accounting entry must have either a debit or a credit.")
        if self.debit is not None and self.credit is not None:
            raise ValueError("An accounting entry cannot have both a debit and a credit.")
        if self.debit is not None and self.debit < 0:
            raise ValueError("A debit value cannot be negative.")
        if self.credit is not None and self.credit < 0:
            raise ValueError("A credit value cannot be negative.")
