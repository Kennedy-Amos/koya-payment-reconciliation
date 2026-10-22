
#!/usr/bin/env python3
"""Reconcile payment events using the latest attempt per transaction."""

import json
from decimal import Decimal

latest = {}

with open("payments.jsonl", encoding="utf-8") as f:
    for line in f:
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        txn_id = event.get("txn_id")
        if not txn_id:
            continue

        ts = event["ts"]

        if txn_id not in latest or ts >= latest[txn_id]["ts"]:
            latest[txn_id] = event

successful = [
    event for event in latest.values()
    if event["status"] == "success"
]

count = len(successful)
total = sum(
    (Decimal(str(event["amount"])) for event in successful),
    Decimal("0")
)

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
