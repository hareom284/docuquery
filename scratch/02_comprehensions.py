"""Day 1, script 2 of 5 — comprehensions.

TASK
  Given ORDERS below, produce two things WITHOUT using append anywhere:
    1. a list of orders over 100
    2. a dict keyed by order id, valued by the whole order

WHAT TO NOTICE
  This replaces array_filter and array_column. Writing an append loop here
  is the tell that you are writing PHP in Python.

DONE WHEN
  Both results print correctly and the word "append" does not appear in this file.
"""

ORDERS = [
    {"id": "A1", "customer": "acme", "total": 250},
    {"id": "A2", "customer": "acme", "total": 80},
    {"id": "A3", "customer": "globex", "total": 140},
    {"id": "A4", "customer": "globex", "total": 35},
]

# TODO: your code here
expensive_orders = [order for order in ORDERS if order["total"] > 100]
orders_by_id = {order["id"]: order for order in ORDERS}

print(expensive_orders)
print(orders_by_id)