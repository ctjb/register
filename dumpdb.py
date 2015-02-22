#!/usr/bin/python
from register import db
from register.models import Person

for p in Person.query:
	print p.serialize()
