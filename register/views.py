from register import app, db
from register.models import Person

from flask import jsonify, make_response, request, render_template
from flask_mail import Mail, Message

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/register', methods = ['POST'])
def register():

	nick = request.form['nick']
	email = request.form['email']
	cabin = request.form['cabin']
	level = request.form['level']
	desc = request.form['desc']
	tshirt = request.form['tshirt']

	price = 0
	if level == 'regular':
		price += 50
	if level == 'sponsor':
		price += 100
	if tshirt != 'shirt-no':
		price += 15

	person = Person(nick, email, cabin, level, desc, tshirt, price)

	db.session.add(person)
	db.session.commit()

	user_id = person.id
	price_czk = price * 28
	price_btc = price / 200.0 + user_id * 0.00000001

	msg = Message("CTJB 2015 Registracia", sender="ctjb@ctjb.net", recipients=[email])
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
ciastka:   %0.8f BTC
adresa:    1AHipWrCLC9HAJaRoYa99e1srG8BHikK2m

Po zaplateni a overeni platby zasleme na email PDF listok.

Sponzorsky program vyhodnotime na konci marca.
""" % (price, user_id, price_czk, user_id, price_btc)
	mail = Mail(app)
	mail.send(msg)

	return render_template('thanks.html', user_id=user_id, price_eur=price, price_czk=price_czk, price_btc=price_btc)

@app.route('/')
def root():
	return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
	return app.send_static_file(path)
