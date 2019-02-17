import hashlib
import os

from main import db


class Person(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    tshirt = db.Column(db.String(128))
    price = db.Column(db.Integer())
    days = db.Column(db.String(128))
    paid = db.Column(db.Boolean())
    token = db.Column(db.String(32))

    def __init__(self, nick, email, tshirt, price, days):
        self.nick = nick
        self.email = email
        self.tshirt = tshirt
        self.price = price
        self.days = days
        self.token = hashlib.sha256(os.urandom(32)).hexdigest()
        self.paid = False

    def serialize(self):
        r = vars(self)
        if "_sa_instance_state" in r:
            del r["_sa_instance_state"]
        return r
