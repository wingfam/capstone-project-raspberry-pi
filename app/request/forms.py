from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import BookingHistory

class ShippingForm(FlaskForm):
    bcode_name = StringField('Mã Booking', validators=[DataRequired()])
    submit = SubmitField('Confirm')
    
    def validate_bcode(self, bcode_name):
        booking_history = BookingHistory.query.filter_by(bcode_name=bcode_name.data).first()
        if booking_history is None:
            raise ValidationError('Mã booking không đúng, xin vui lòng nhập lại.')
    
class PickupForm(FlaskForm):
    unlock_code = StringField('Unlock Code', validators=[DataRequired()])
    submit = SubmitField('Confirm')