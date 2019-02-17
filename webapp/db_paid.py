#!/usr/bin/env python3
from main import db
from models import Person

num = int(input("User ID: "))
p = Person.query.get(num)

if p:
    p.paid = True
    email = p.email
    db.session.commit()
    print("User %d (%s) marked as paid" % (num, email))
else:
    print("User %d not found" % num)
