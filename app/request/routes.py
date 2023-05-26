from flask import render_template, flash, redirect, url_for, request
from app import db
from app.models import Locker, BookingOrder, BookingCode, BookingHistory
from app.request import bp
from app.request.forms import ShippingForm, PickupForm
from werkzeug.urls import url_parse
from datetime import datetime

@bp.route('/shipping', methods=['GET', 'POST'])
def shipping():
    form = ShippingForm()
    if form.validate_on_submit():
        current_time = datetime.now()
        booking_code = BookingCode.query.filter_by(bcode_name=form.bcode_name.data).first()
        valid_date = booking_code.bcode_valid_date
        
        if booking_code is None:
            flash('Mã booking không đúng, vui lòng nhập lại.')
            return redirect(url_for('request.shipping'))
        elif valid_date < current_time:
            flash('Mã booking đã hết hạn, vui lòng tạo booking khác.')
            return redirect(url_for('request.shipping'))
            
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('request.success', isSuccess='shipping-success')
        return redirect(next_page)
    
    return render_template('request/shipping.html', title='Shipping', form=form)

@bp.route('/pickup', methods=['GET', 'POST'])
def pickup():
    form = PickupForm()
    if form.validate_on_submit():
        current_time = datetime.now()
        history = BookingHistory.query.filter_by(unlock_code=form.unlock_code.data).first()
        locker = Locker.query.filter_by(locker_name=history.locker_name).first()
        
        if history.unlock_code is None:
            flash('Mã unlock không đúng, vui lòng nhập lại')
            return redirect(url_for('request.pickup'))
        elif locker.ucode_valid_date < current_time:
            flash('Mã unlock đã hết hạn, vui lòng tạo booking khác')
            return redirect(url_for('request.pickup'))
            
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('request.success', isSuccess='pickup-success')
        return redirect(next_page)
    
    return render_template('request/pickup.html', title='Pickup', form=form)

@bp.route('/success/<isSuccess>', methods=['GET', 'POST'])
def success(isSuccess):
    return render_template('request/success.html', title='Success', isSuccess=isSuccess)
