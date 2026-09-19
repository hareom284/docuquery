"""Day 1, script 3 of 5 — dataclasses and unenforced type hints.

TASK
  Define @dataclass Order with: id: str, total: int, customer: str
  Create a valid one and print it.
  Then DELIBERATELY create one with total="not a number" and print it too.

WHAT TO NOTICE
  The second one does not raise. In PHP a typed property would throw here.
  Python annotations are metadata; nothing checks them at runtime.
  This is the entire reason Pydantic exists, which is tomorrow's topic.

DONE WHEN
  Both print, nothing raises, and you can say out loud why.
"""

# TODO: your code here

from dataclasses import dataclass

@dataclass
class Order:
    id: str
    total: int
    customer: str

# Create a valid order
valid_order = Order(id="1", total=100, customer="Alice")
print(valid_order)

# Create an invalid order (total is a string)
invalid_order = Order(id="2", total="not a number", customer="Bob")
print(invalid_order)