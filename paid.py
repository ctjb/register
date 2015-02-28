#!/usr/bin/python
from register import db
from register.models import Person

import os
import sys
import StringIO
import qrcode
import base64

def qrdata(value):
	buf = StringIO.StringIO()
	img = qrcode.make(value)
	img.save(buf, 'PNG')
	return base64.b64encode(buf.getvalue())

num = input('User ID: ')
p = Person.query.get(num)
if not p:
	print 'Not found'
	sys.exit(1)

p.paid = True
token = p.token
db.session.commit()

print num, token

t = open('ticket.svg', 'r').read()
f = open('ticket_%d.svg' % num, 'w')
t = t.replace('@@QR_CODE_IMAGE@@', qrdata(token))
t = t.replace('@@QR_CODE_TEXT_1@@', token[:32])
t = t.replace('@@QR_CODE_TEXT_2@@', token[32:])
f.write(t)
f.close()

os.system('inkscape ticket_%d.svg --export-pdf=ticket_%d.pdf --export-text-to-path' % (num, num))
os.unlink('ticket_%d.svg' % num)
