import datetime
from flask import render_template
from flask_login import login_required
from app.main import bp
from app.models import Resident, BookingOrder

@bp.route('/')
@bp.route('/main.index')
def index():
    current_datetime = datetime.datetime.now()
    return render_template('index.html', title='Home', current_datetime=current_datetime)

@bp.route('/resident/<phone>')
def resident(phone):
    resident = Resident.query.filter_by(phone=phone).first_or_404()
    bookings = resident.booking_order.order_by(BookingOrder.booking_date.desc())
    
    return render_template('resident.html', resident=resident, bookings=bookings)