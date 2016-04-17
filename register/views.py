from register import app, db
from register.models import Person

from flask import make_response, request, render_template, copy_current_request_context
from flask_mail import Mail, Message

import qrcode
import StringIO
import base64

from threading import Thread

def send_mail_async(app, msg):

	@copy_current_request_context
	def send_mail(app, msg):
		mail = Mail(app)
		mail.send(msg)

	t = Thread(target=send_mail, args = (app, msg))
	t.start()

@app.errorhandler(404)
def not_found(error):
	return make_response('Not found', 404)

@app.route('/count', methods = ['GET'])
def count():
	cnt_total = Person.query.count()
	cnt_paid = Person.query.filter(Person.paid == True).count()
	res = '%d/%d' % (cnt_paid, cnt_total)
	return make_response(res, 200)

@app.route('/', methods = ['POST'])
def register():

	nick = request.form['nick']
	email = request.form['email']
	if 'desc' in request.form:
		desc = request.form['desc']
	else:
		desc = ''
	tshirt = request.form['tshirt']

	cabin = 0
	level = 'regular'
	price = 40
	if tshirt != 'shirt-no':
		price += 15

	person = Person(nick, email, cabin, level, desc, tshirt, price)

	db.session.add(person)
	db.session.commit()

	user_id = person.id
	price_czk = price * 27.50
	price_btc = int(price * 100000 / 375) * 1.0 / 100000 + user_id * 0.00000001 # last 3 decimals of price are user ID

	msg = Message("CTJB 2016 Registracia", sender="ctjb@ctjb.net", recipients=[email])
	msg.body = """
Dakujeme za registraciu!

Platba v Eurach
---------------
ciastka:             %d EUR
cislo uctu:          2700158887 / 8330
variabilny symbol:   %d

Platba v Ceskych Korunach
-------------------------
ciastka:             %d CZK
cislo uctu:          2700158887 / 2010
variabilny symbol:   %d

Platba v Bitcoinoch
-------------------
ciastka:   %0.8f BTC (posielajte presne!)
adresa:    14R3dXhbsnStDwhyrNY8LN6ZRZ2PefKb2W

Po zaplateni a overeni platby zasleme na email PDF listok.
""" % (price, user_id, price_czk, user_id, price_btc)

	send_mail_async(app, msg)

	buf = StringIO.StringIO()
	img = qrcode.make('bitcoin:14R3dXhbsnStDwhyrNY8LN6ZRZ2PefKb2W?amount=%0.8f' % price_btc)
	img.save(buf, 'PNG')
	qrdata = 'data:image/png;base64,' + base64.b64encode(buf.getvalue())

	return render_template('thanks.html', user_id=user_id, price_eur=price, price_czk=price_czk, price_btc=price_btc,qrcode=qrdata)

@app.route('/', methods = ['GET'])
def root():
	return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
	return app.send_static_file(path)
