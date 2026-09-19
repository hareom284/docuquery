"""Day 1, script 4 of 5 — JSON and KeyError.

TASK
  json.loads the RAW string below.
  Print the second line item's description.
  Then try to read a key that does not exist and catch the KeyError.

WHAT TO NOTICE
  Missing dict keys raise. PHP would hand you a warning and null.
  Loud failure is the default here, and that is a feature.

DONE WHEN
  The description prints and the missing key is caught, not crashed on.
"""

import json

RAW = '''
{
  "invoice_no": "INV-2026-001",
  "vendor": {"name": "Acme Ltd", "country": "TH"},
  "line_items": [
    {"desc": "Consulting", "qty": 2, "unit_price": 500},
    {"desc": "Hosting", "qty": 12, "unit_price": 25}
  ]
}
'''

# TODO: your code here

data = json.loads(RAW)
print(data["line_items"][1]["desc"])  # Print the second line item's description

try:
    print(data["non_existent_key"])
except KeyError as e:
    print(f"KeyError caught: {e}")