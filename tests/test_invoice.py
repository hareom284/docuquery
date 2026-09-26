"""Day 2, part 3 — five tests.

Run them with:   uv run pytest -q

Two tests must PASS with good data. Three must raise ValidationError.
`pytest.raises` is the Python version of PHPUnit's expectException.

Import your models from the file you wrote:
    import sys; sys.path.append("scratch")     # already done below
    from importlib import import_module
    models = import_module("07_invoice_validators")

DONE WHEN
  `uv run pytest -q` shows 5 passed.
"""

import sys
from importlib import import_module
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.append(str(Path(__file__).resolve().parent.parent / "scratch"))
models = import_module("07_invoice_validators")
Invoice = models.Invoice
LineItem = models.LineItem


def valid_payload():
    """One good invoice as a plain dict. Tests copy it and break one thing."""
    return {
        "invoice_no": "INV-2026-001",
        "issued_on": "2026-01-31",
        "line_items": [
            {"desc": "Consulting", "qty": 2, "unit_price": "500.00"},
            {"desc": "Hosting", "qty": 12, "unit_price": "25.00"},
        ],
        "total": "1300.00",
    }


# TEST 1 (must pass) — a valid invoice validates, and qty became a real int.
def test_valid_invoice():
    invoice = Invoice.model_validate(valid_payload())
    # TODO: assert the invoice_no is right, and that the first qty == 2
    assert invoice.invoice_no == "INV-2026-001"
    assert invoice.line_items[0].qty == 2


# TEST 2 (must pass) — model_dump() gives back a plain dict.
def test_model_dump():
    invoice = Invoice.model_validate(valid_payload())
    # TODO: dump = invoice.model_dump()  then assert dump["invoice_no"] == ...
    dump = invoice.model_dump()
    assert dump["invoice_no"] == "INV-2026-001"


# TEST 3 (must raise) — qty of 0 is rejected by the field validator.
def test_qty_must_be_positive():
    payload = valid_payload()
    payload["line_items"][0]["qty"] = 0
    # TODO: with pytest.raises(ValidationError): Invoice.model_validate(payload)
    with pytest.raises(ValidationError):
        Invoice.model_validate(payload)


# TEST 4 (must raise) — a total that does not match the line items.
def test_total_must_match():
    payload = valid_payload()
    payload["total"] = "999.00"
    # TODO: same shape as test 3
    with pytest.raises(ValidationError):
        Invoice.model_validate(payload)


# TEST 5 (must raise) — a date that is not a date.
def test_bad_date():
    payload = valid_payload()
    payload["issued_on"] = "not a date"
    # TODO: same shape as test 3
    with pytest.raises(ValidationError):
        Invoice.model_validate(payload)
