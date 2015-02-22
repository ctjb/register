#!/usr/bin/python
from register import db
from register.models import Person

db.create_all()
db.session.commit()
