from flask import current_app
from datetime import datetime, timedelta
from time import time
import jwt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

@login.user_loader
def load_resident(id):
    return Resident.query.get(int(id))

class Resident(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    booking_order = db.relationship('BookingOrder', backref='resident', lazy='dynamic')
    package_info = db.relationship('PackageInfo', backref='resident', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Resident.query.get(id)
    
    def __repr__(self):
        return '<resident {}>'.format(self.phone)

class Locker(db.Model):
    valid_date = datetime.now() + timedelta(days=3)
    
    id = db.Column(db.Integer, primary_key=True)
    locker_name = db.Column(db.String(64), index=True, nullable=False)
    locker_status = db.Column(db.Boolean, default=True)
    unlock_code = db.Column(db.String(64))
    ucode_valid_date = db.Column(db.DateTime, default=valid_date)
    booking_order = db.relationship('BookingOrder', backref='locker', lazy='dynamic')
    package_info = db.relationship('PackageInfo', backref='locker', lazy='dynamic')
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

    def __repr__(self):
        return '<BookingOrder {}>'.format(self.booking_date)

class BookingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bcode_name = db.Column(db.String(64), index=True, nullable=False)
    locker_name = db.Column(db.String(64), index=True, nullable=False)
    unlock_code = db.Column(db.String(64))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking_order.id'))
    
    def __repr__(self):
        return '<BookingHistory {}>'.format(self.bcode_name)

class BookingCode(db.Model):
    valid_date = datetime.now() + timedelta(minutes=10)
    
    id = db.Column(db.Integer, primary_key=True)
    bcode_name = db.Column(db.String(64), index=True, nullable=False)
    bcode_valid_date = db.Column(db.DateTime, index=True, default=valid_date)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking_order.id'))
    
    def __repr__(self):
        return '<BookingCode {}>'.format(self.bcode_valid_date)
    
class PackageInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_date = db.Column(db.DateTime, index=True)
    pickup_date = db.Column(db.DateTime, index=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'))
    locker_id = db.Column(db.Integer, db.ForeignKey('locker.id'))
    
    def __repr__(self):
        return '<PackageInfo {}>'.format(self.id)