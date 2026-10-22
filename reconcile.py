
#!/usr/bin/env python3
"""Payment reconciliation."""

import json
from decimal import Decimal, InvalidOperation

latest = {}

with open("payments.jsonl", encoding="utf-8") as f:
    for line in f:
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        txn_id = event.get("txn_id")
        ts = event.get("ts")

        if not txn_id or ts is None:
            continue

        if txn_id not in latest or ts >= latest[txn_id].get("ts", ""):
            latest[txn_id] = event

successful = [
    event for event in latest.values()
    if event.get("status") == "success"
]

count = len(successful)
total = Decimal("0")

for event in successful:
    try:
        amount = Decimal(str(event["amount"]))
        if amount.is_finite():
            total += amount
    except (KeyError, ValueError, TypeError, InvalidOperation):
        continue

with open("expected.txt", encoding="utf-8") as f:
    expected = int(f.read().strip())

if count != expected:
    print(
        f"Check failed: counted {count} successful payments, "
        f"expected {expected}."
    )
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
