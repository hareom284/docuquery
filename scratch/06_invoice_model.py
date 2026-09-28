"""Day 2, part 1 of 2 — Pydantic models.

TASK
  Build two models that describe an invoice:

    LineItem: desc (str), qty (int), unit_price (Decimal)
    Invoice:  invoice_no (str), issued_on (date),
              line_items (list of LineItem), total (Decimal)

  Then, at the bottom:
    1. Build a VALID invoice from the RAW dict below with Invoice.model_validate(RAW).
       Print it.
    2. Try Invoice.model_validate(BAD) inside try/except ValidationError.
       Print the error.

WHAT TO NOTICE
  Yesterday a @dataclass accepted total="not a number" without complaining.
  Pydantic reads the same type hints and actually ENFORCES them.
  Notice too that "2" becomes 2 and "2026-01-31" becomes a real date object:
  Pydantic converts when it safely can, and raises when it cannot.

DONE WHEN
  The valid invoice prints, and the bad one raises a ValidationError that you catch.
"""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ValidationError

RAW = {
    "invoice_no": "INV-2026-001",
    "issued_on": "2026-01-31",
    "line_items": [
        {"desc": "Consulting", "qty": "2", "unit_price": "500.00"},
        {"desc": "Hosting", "qty": 12, "unit_price": "25.00"},
    ],
    "total": "1300.00",
}

BAD = {
    "invoice_no": "INV-2026-002",
    "issued_on": "not a date",
    "line_items": [],
    "total": "not a number",
}

# TODO: your code here
class LineItem(BaseModel):
    desc: str
    qty: int
    unit_price: Decimal 
    
    
class Invoice(BaseModel):
    invoice_no: str
    issued_on: date
    line_items: list[LineItem]
    total: Decimal
    
invoice = Invoice.model_validate(RAW)
print(invoice)

try:
    invoice = Invoice.model_validate(BAD)
except ValidationError as e:
    print(e)

