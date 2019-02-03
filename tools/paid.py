#!/usr/bin/python
from register import db
from register.models import Person

import os
import sys
import StringIO
import qrcode
import base64

num = input('User ID: ')
p = Person.query.get(num)

if p:
	p.paid = True
	email = p.email
	db.session.commit()
	print 'User %d (%s) marked as paid' % (num, email)
