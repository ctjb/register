#!/usr/bin/env python3
from main import db

db.create_all()
db.session.commit()
