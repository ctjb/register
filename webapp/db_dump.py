#!/usr/bin/env python3
import sys

import btc
from main import db
from models import Person

paid_only = len(sys.argv) > 1 and sys.argv[1] == "paid"
unpaid_only = len(sys.argv) > 1 and sys.argv[1] == "unpaid"

for p in Person.query:
    if paid_only and not p.paid:
        continue
    if unpaid_only and p.paid:
        continue
    j = p.serialize()
    j["btc"] = btc.addresses[p.id]
    print(j)
