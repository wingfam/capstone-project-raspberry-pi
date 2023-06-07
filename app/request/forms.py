from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DeliveryForm(FlaskForm):
    bcode = StringField('Nhập mã booking', validators=[DataRequired()])
    submit = SubmitField('Xác Nhận')
    
class PickupForm(FlaskForm):
    ucode = StringField('Nhập mã unlock', validators=[DataRequired()])
    submit = SubmitField('Xác Nhận')
        
class EmptyForm(FlaskForm):
    booking_id = StringField('booking_id')
    booking_code = StringField('booking_code')
    locker_name = StringField('locker_name')
    unlock_code = StringField('unlock_code')
    submit = SubmitField('Xác Nhận')