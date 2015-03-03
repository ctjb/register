#!/usr/bin/python
from register import db
from register.models import Person

import os
import sys
import StringIO
import qrcode
import base64

GEN_TICKETS = len(sys.argv) > 1

def qrdata(value):
	buf = StringIO.StringIO()
	img = qrcode.make(value)
	img.save(buf, 'PNG')
	return base64.b64encode(buf.getvalue())

if GEN_TICKETS:
	t = open('ticket.svg', 'r').read()

print 'Attendees:'
for p in Person.query.filter(Person.paid == True):
	print p.id, p.token, p.email
	if GEN_TICKETS:
		tt = t
		tt = tt.replace('@@QR_CODE_IMAGE@@', qrdata(p.token))
		tt = tt.replace('@@QR_CODE_TEXT_1@@', p.token[:32])
		tt = tt.replace('@@QR_CODE_TEXT_2@@', p.token[32:])
		f = open('tickets/ticket_%d.svg' % p.id, 'w')
		f.write(tt)
		f.close()
		os.system('inkscape tickets/ticket_%d.svg --export-pdf=tickets/ticket_%d.pdf --export-text-to-path' % (p.id, p.id))
		os.unlink('tickets/ticket_%d.svg' % p.id)
		open('tickets/ticket_%d.txt' % p.id, 'w').write(p.email)
