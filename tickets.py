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
		fn = 'ticket_%03d_%s' % (p.id, p.email)
		if os.path.isfile('tickets/%s.pdf' % fn):
			continue
		tt = t
		tt = tt.replace('@@QR_CODE_IMAGE@@', qrdata(p.token))
		tt = tt.replace('@@QR_CODE_TEXT_1@@', p.token[:32])
		tt = tt.replace('@@QR_CODE_TEXT_2@@', p.token[32:])
		f = open('tickets/%s.svg' % fn, 'w')
		f.write(tt)
		f.close()
		os.system('inkscape tickets/%s.svg --export-pdf=tickets/%s.pdf --export-text-to-path' % (fn, fn))
		os.unlink('tickets/%s.svg' % fn)
