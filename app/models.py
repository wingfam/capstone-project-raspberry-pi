from flask import current_app
from datetime import datetime, timedelta
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
# from app import db, login

# @login.user_loader
# def load_resident(id):
#     return Resident.query.get(int(id))

class System(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<system {}>'.format(self.email)

class Resident(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    booking_order = db.relationship('BookingOrder', backref='resident', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # def get_reset_password_token(self, expires_in=600):
    #     return jwt.encode(
    #         {'reset_password': self.id, 'exp': time() + expires_in},
    #         current_app.config['SECRET_KEY'], algorithm='HS256')

    # @staticmethod
    # def verify_reset_password_token(token):
    #     try:
    #         id = jwt.decode(token, current_app.config['SECRET_KEY'],
    #                         algorithms=['HS256'])['reset_password']
    #     except:
    #         return
    #     return Resident.query.get(id)
    
    def __repr__(self):
        return '<resident {}>'.format(self.phone)

class Locker(db.Model):
    valid_date = datetime.now() + timedelta(days=3)
    
    id = db.Column(db.Integer, primary_key=True)
    locker_name = db.Column(db.String(64), index=True, nullable=False)
    locker_status = db.Column(db.Boolean, default=True)
    booking_order = db.relationship('BookingOrder', backref='locker', lazy='dynamic')
    access_warning = db.relationship('AccessWarning', backref='locker', lazy='dynamic')

    def __repr__(self):
        return '<Locker {}>'.format(self.locker_name)
    
class AccessWarning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(128), nullable=True)
    create_date = db.Column(db.DateTime, default=datetime.now())
    locker_id = db.Column(db.Integer, db.ForeignKey('locker.id'))

class BookingOrder(db.Model):
    valid_date = datetime.now() + timedelta(days=3)
    
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, index=True, default=datetime.now())
    booking_valid_date = db.Column(db.DateTime, index=True, default=valid_date)
    booking_status = db.Column(db.Boolean, default=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'))
    locker_id = db.Column(db.Integer, db.ForeignKey('locker.id'))
    booking_history = db.relationship('BookingHistory', backref='booking', lazy='dynamic')
    booking_code = db.relationship('BookingCode',  backref='booking', lazy='dynamic')
    unlock_code = db.relationship('UnlockCode',  backref='booking', lazy='dynamic')

    def __repr__(self):
        return '<BookingOrder {}>'.format(self.booking_date)

class BookingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bcode_name = db.Column(db.String(64), index=True, nullable=False)
    locker_name = db.Column(db.String(64), index=True, nullable=False)
    unlock_code = db.Column(db.String(64))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking_order.id'))
    
    def __repr__(self):
        return '<BookingHistory {}>'.format(self.id, self.bcode_name, self.unlock_code)

class BookingCode(db.Model):
    valid_date = datetime.now() + timedelta(minutes=10)
    
    id = db.Column(db.Integer, primary_key=True)
    bcode_name = db.Column(db.String(64), index=True, nullable=False)
    bcode_create_date = db.Column(db.DateTime, index=True, default=datetime.now())
    bcode_valid_date = db.Column(db.DateTime, index=True, default=valid_date)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking_order.id'))
    
    def __repr__(self):
        return '<BookingCode {}>'.format(self.bcode_name)
    
class UnlockCode(db.Model):
    valid_date = datetime.now() + timedelta(days=3)
    
    id = db.Column(db.Integer, primary_key=True)
    ucode_name = db.Column(db.String(64), index=True, nullable=False)
    ucode_create_datetime = db.Column(db.DateTime, index=True, default=datetime.now())
    ucode_valid_datetime = db.Column(db.DateTime, index=True, default=valid_date)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking_order.id'))
    
    def __repr__(self):
        return '<UnlockCode {}>'.format(self.ucode_name)