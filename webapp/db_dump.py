#!/usr/bin/env python
import sys

from main import db
from models import Person

paid_only = len(sys.argv) > 1 and sys.argv[1] == "paid"

for p in Person.query:
    if paid_only and not p.paid:
        continue
    print(p.serialize())
