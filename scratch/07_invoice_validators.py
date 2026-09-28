"""Day 2, part 2 of 2 — validators.

TASK
  Copy your LineItem and Invoice from 06_invoice_model.py, then add:

    1. A FIELD validator on LineItem.qty that rejects qty < 1.
       @field_validator("qty")
       @classmethod
       def qty_must_be_positive(cls, v): ...raise ValueError(...) or return v

    2. A MODEL validator that checks the invoice total equals the sum of
       qty * unit_price over all line items.
       @model_validator(mode="after")
       def total_must_match(self): ...raise ValueError(...) or return self

  At the bottom, print Invoice.model_json_schema() — you need this output on Day 10,
  when you ask an LLM to return structured data.

WHAT TO NOTICE
  A FIELD validator sees ONE field and cannot see the others.
  A MODEL validator runs after every field is valid, so it can compare fields.
  Cross-field rules always need a model validator.

DONE WHEN
  A negative qty raises, a wrong total raises, a correct invoice passes,
  and the JSON schema prints.
"""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ValidationError, field_validator, model_validator

# TODO: your code here
RAW = {
    "invoice_no": "INV-2026-001",
    "issued_on": "2026-01-31",
    "line_items": [
        {"desc": "Consulting", "qty": "2", "unit_price": "500.00"},
        {"desc": "Hosting", "qty": 12, "unit_price": "25.00"},
    ],
    "total": "1300.00",
}


class LineItem(BaseModel):
    desc: str
    qty: int
    unit_price: Decimal

    @field_validator("qty")
    @classmethod
    def qty_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("Quantity must be positive")
        return v


class Invoice(BaseModel):
    invoice_no: str
    issued_on: date
    line_items: list[LineItem]
    total: Decimal

    @model_validator(mode="after")
    def total_must_match(self):
        calculated_total = sum(item.qty * item.unit_price for item in self.line_items)
        if self.total != calculated_total:
            raise ValueError(f"Total {self.total} does not match calculated total {calculated_total}")
        return self


try:
    invoice = Invoice.model_validate(RAW)
    print(invoice)
except ValidationError as e:
    print(e)
  
print(Invoice.model_json_schema())