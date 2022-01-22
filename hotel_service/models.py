# models.py

from datetime import datetime, timedelta
from flask_login import UserMixin
from . import db

def default_date():
    return datetime.now().strftime('%m-%d-%Y')

class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(256), unique=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(1024))
    reservations = db.Column(db.PickleType, default=[])

class HotelRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    address = db.Column(db.String(256))
    country = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zipcode = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    # Room Fields
    qty = db.Column(db.Integer)
    room_size = db.Column(db.Integer)
    max_persons = db.Column(db.Integer, default=1)
    max_adults = db.Column(db.Integer, default=1)
    max_children = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    # Room Properties
    ameneties = db.Column(db.PickleType, default={})
    smoking_allowed = db.Column(db.Boolean, default=False)
    pets_allowed = db.Column(db.Boolean, default=False)
    check_in = db.Column(db.DateTime, default=None, nullable=True)
    check_out = db.Column(db.DateTime, default=None, nullable=True)
    reserved = db.Column(db.Boolean, default=False)
    reserved_by = db.Column(db.String(256), default=None, nullable=True)
