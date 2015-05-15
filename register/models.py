from register import db
import os
import hashlib

class Person(db.Model):

	id    = db.Column(db.Integer,     primary_key = True)
	nick  = db.Column(db.String(128))
	email = db.Column(db.String(128), unique=True)
	cabin = db.Column(db.String(128))
	level = db.Column(db.String(128))
	desc = db.Column(db.String(1024))
	tshirt = db.Column(db.String(128))
	price = db.Column(db.Integer())
	paid = db.Column(db.Boolean())
	token = db.Column(db.String(32))

	def __init__(self, nick, email, cabin, level, desc, tshirt, price):
		self.nick = nick
		self.email = email
		self.cabin = cabin
		self.level = level
		self.desc = desc
		self.tshirt = tshirt
		self.price = price
		self.token = hashlib.sha256(os.urandom(32)).hexdigest()
		self.paid = False

	def serialize(self):
		r = {}
		for k, v in vars(self).iteritems():
			if not k.startswith('_') and v:
					r[k] = v
		return r
