import base64
from io import BytesIO
from threading import Thread

import qrcode
import requests
from flask import copy_current_request_context, make_response, render_template, request
from flask_mail import Mail, Message

from main import app, db
from models import Person
import btc


def get_price_satoshi(euros):
    try:
        price = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur"
        ).json()["bitcoin"]["eur"]
        # sanity check
        assert price > 2000 and price < 10000
        return int(100000000 * euros / price)
    except:
        return None


def send_mail_async(app, msg):
    @copy_current_request_context
    def send_mail(app, msg):
        mail = Mail(app)
        mail.send(msg)

    t = Thread(target=send_mail, args=(app, msg))
    t.start()


@app.errorhandler(404)
def not_found(error):
    return make_response("Not found", 404)


@app.route("/count", methods=["GET"])
def count():
    cnt_total = Person.query.count()
    cnt_paid = Person.query.filter(Person.paid == True).count()
    res = "%d/%d" % (cnt_paid, cnt_total)
    return make_response(res, 200)


@app.route("/", methods=["POST"])
def register():

    price = get_price_satoshi(euros=60)
    if not price:
        return make_response("Price fail", 500)

    nick = request.form["nick"]
    email = request.form["email"]
    tshirt = request.form["tshirt"]

    days = ""
    for i in range(1, 6):
        field = "day%d" % i
        if field in request.form:
            days += "X"
        else:
            days += "."

    person = Person(nick=nick, email=email, tshirt=tshirt, price=price, days=days)

    db.session.add(person)
    db.session.commit()

    try:
        btc_address = btc.addresses[person.id]
    except:
        return make_response("Address fail", 500)
    btc_price = "%0.8f" % (price / 100000000)

    """
    msg = Message("CTJB 2019 Registracia", sender="ctjb@ctjb.net", recipients=[email])
    msg.body = render_template(
        "registered.txt", btc_address=btc_address, btc_price=btc_price
    )
    send_mail_async(app, msg)
    """

    qr_uri = "bitcoin:{btc_address}?amount={btc_price}".format(
        btc_address=btc_address, btc_price=btc_price
    )
    buf = BytesIO()
    img = qrcode.make(qr_uri)
    img.save(buf, format="PNG")
    btc_qrcode = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return render_template(
        "registered.html",
        btc_address=btc_address,
        btc_price=btc_price,
        btc_qrcode=btc_qrcode,
    )


@app.route("/", methods=["GET"])
def root():
    return app.send_static_file("index.html")


@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)
