from register import app, db
from register.models import Person

from flask import jsonify, make_response, request, render_template

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

	return render_template('thanks.html', user_id=person.id, price_eur=price, price_czk=price*28, price_btc=price/200.0+person.id*0.00000001)

@app.route('/')
def root():
	return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
	return app.send_static_file(path)
