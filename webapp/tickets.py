#!/usr/bin/env python3
import base64
from io import BytesIO
import os
import sys

import qrcode
from main import db
from models import Person

GEN_TICKETS = len(sys.argv) > 1


def qrdata(value):
    buf = BytesIO()
    img = qrcode.make(value)
    img.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


if GEN_TICKETS:
    t = open("ticket.svg", "r").read()

print("Attendees:")
for p in Person.query.filter(Person.paid == True):
    is_new = False
    if GEN_TICKETS:
        fn = "ticket_%03d_%s" % (p.id, p.email)
        if not os.path.isfile("tickets/%s.pdf" % fn):
            tt = t
            tt = tt.replace("@@QR_CODE_IMAGE@@", qrdata(p.token))
            tt = tt.replace("@@QR_CODE_TEXT_1@@", p.token[:32])
            tt = tt.replace("@@QR_CODE_TEXT_2@@", p.token[32:])
            f = open("tickets/%s.svg" % fn, "w")
            f.write(tt)
            f.close()
            os.system(
                "inkscape tickets/%s.svg --export-pdf=tickets/%s.pdf --export-text-to-path"
                % (fn, fn)
            )
            os.unlink("tickets/%s.svg" % fn)
            is_new = True
    print(p.id, p.token, p.email, "!!! NEW !!!" if is_new else "")
