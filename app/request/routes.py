from flask import render_template, flash, redirect, url_for, request
from app import db
from app.models import Locker, BookingOrder, BookingCode, BookingHistory, UnlockCode
from app.request import bp
from app.request.forms import DeliveryForm, PickupForm, EmptyForm
from app.auth.routes import firebase_login
from app.firebase_config import firebaseDB
from werkzeug.urls import url_parse
from datetime import datetime
from requests.exceptions import ConnectionError
import random
import math


@bp.route("/delivery", methods=["GET", "POST"])
def delivery():
    form = DeliveryForm()
    if form.validate_on_submit():
        current_datetime = datetime.now()
        try:
            # Login vào firebase mỗi lần gửi yêu cầu để tránh bị timeout
            smart_locker = firebase_login()

            fb_booking_code = firebaseDB.child("booking_code").order_by_child(
                "bcode_name").equal_to(form.bcode.data).get(smart_locker["idToken"])
            items = list(fb_booking_code.val().items())
            
            valid_datetime = datetime.strptime(items[0][1].get(
                "bcode_valid_datetime"), "%Y-%m-%d %H:%M:%S")

            if current_datetime > valid_datetime:
                flash("Mã booking đã hết hạn, vui lòng tạo booking khác.")
                return redirect(url_for("request.delivery"))

            booking_id = items[0][1].get("booking_id")
            booked_locker = firebaseDB.child(
                "booking_order/", booking_id, "/locker_id").get(smart_locker["idToken"]).val()
            booked_locker_name = firebaseDB.child(
                "locker/", booked_locker, "/locker_name").get(smart_locker["idToken"]).val()
        except IndexError:
            flash("Mã booking không đúng, vui lòng nhập lại.")
            return redirect(url_for("request.delivery"))
        except ConnectionError:
            db_booking_code = BookingCode.query.filter_by(
                bcode_name=form.bcode.data).first()

            if db_booking_code is None:
                flash("Mã booking không đúng, vui lòng nhập lại.")
                return redirect(url_for("request.delivery"))

            valid_datetime = db_booking_code.bcode_valid_date
            if current_datetime > valid_datetime:
                flash("Mã booking đã hết hạn, vui lòng tạo booking khác.")
                return redirect(url_for("request.delivery"))

            booking_id = BookingOrder.query.get(db_booking_code.booking_id)
            booked_locker = Locker.query.get(booking_id.locker_id)
            booked_locker_name = booked_locker.locker_name

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for(
                "request.show_locker", task="delivery",
                booking_id=booking_id, booked_locker_name=booked_locker_name,
                booking_code=form.bcode.data
            )
            return redirect(next_page)

    return render_template("request/delivery.html", title="Delivery", form=form)

@bp.route("/pickup", methods=["GET", "POST"])
def pickup():
    form = PickupForm()
    if form.validate_on_submit():
        current_datetime = datetime.now()
        try:
            # Login vào firebase mỗi lần gửi yêu cầu để tránh bị timeout
            smart_locker = firebase_login()

            fb_unlock_code = firebaseDB.child("unlock_code").order_by_child(
                "ucode_name").equal_to(form.ucode.data).get(smart_locker["idToken"])
            items = list(fb_unlock_code.val().items())
            booking_id = items[0][1].get("booking_id")
            valid_datetime = firebaseDB.child(
                "booking_order/", booking_id, "/booking_valid_datetime").get(smart_locker["idToken"])
            valid_datetime = datetime.strptime(
                valid_datetime.val(), "%Y-%m-%d %H:%M:%S")

            if current_datetime > valid_datetime:
                flash("Mã unlock đã hết hạn, vui lòng tạo booking khác")
                return redirect(url_for("request.pickup"))

            booking_status = firebaseDB.child(
                "booking_order/", booking_id, "/booking_status").get(smart_locker["idToken"])
            if booking_status.val() is False:
                flash("Booking đã hết hạn, vui lòng tạo booking khác")
                return redirect(url_for("request.pickup"))

            booked_locker = firebaseDB.child(
                "booking_order/", booking_id, "/locker_id").get(smart_locker["idToken"]).val()
            booked_locker_name = firebaseDB.child(
                "locker/", booked_locker, "/locker_name").get(smart_locker["idToken"]).val()
        except IndexError:
            flash("Mã unlock không đúng, vui lòng nhập lại.")
            return redirect(url_for("request.pickup"))
        except ConnectionError:
            db_history = BookingHistory.query.filter_by(
                unlock_code=form.ucode.data).first()
            db_unlock_code = UnlockCode.query.filter_by(
                ucode_name=form.ucode.data).first()

            if db_unlock_code is None:
                flash("Mã booking không đúng, vui lòng nhập lại.")
                return redirect(url_for("request.pickup"))

            if db_unlock_code.ucode_valid_datetime < current_datetime:
                flash("Mã unlock đã hết hạn, vui lòng tạo booking khác")
                return redirect(url_for("request.pickup"))

            booking_id = db_history.booking_id
            booked_locker_name = db_history.locker_name

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for(
                "request.show_locker", task="pickup",
                booking_id=booking_id,
                booked_locker_name=booked_locker_name,
            )
        return redirect(next_page)

    return render_template("request/pickup.html", title="Pickup", form=form)


@bp.route("/show_locker/<task>/<booking_id>/<booked_locker_name>", methods=["GET", "POST"])
def show_locker(task, booked_locker_name, booking_id):
    form = EmptyForm()
    lockers = Locker.query.all()
    if form.validate_on_submit():
        smart_locker = firebase_login()

        if task == "delivery":
            print("Delivery completed!")
        elif task == "pickup":
            new_booking_status = False
            firebaseDB.child("/booking_order/", booking_id).update(
                {"booking_status": new_booking_status}, smart_locker["idToken"])
            print("Pickup completed!")

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("request.success")
            return redirect(next_page)
    return render_template(
        "request/show_locker.html", title="Locker Position", task=task,
        lockers=lockers, booked_locker_name=booked_locker_name,
        booking_id=booking_id, form=form
    )


@bp.route("/success", methods=["GET", "POST"])
def success():
    return render_template("request/success.html", title="Success"), {"Refresh": "3; url=http://127.0.0.1:5000/main.index"}

# Generate random 6 digits code
def generate_random_6_digits():
    # storing strings in a list
    digits = [i for i in range(0, 10)]
    # initializing a string
    random_str = ""
    # we can generate any lenght of string we want
    for i in range(6):
        # generating a random index
        # if we multiply with 10 it will generate a number between 0 and 10 not including 10
        # multiply the random.random() with length of your base list or str
        i = math.floor(random.random() * 10)
        random_str += str(digits[i])
    return random_str
