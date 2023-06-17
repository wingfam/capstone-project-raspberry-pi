from flask import render_template, flash, redirect, url_for
from app import db
from app.firebase_config import firebaseApp, identity
from app.models import Resident
from app.auth import bp
from app.auth.forms import RegistrationForm

def firebase_login():
    firebaseAuth = firebaseApp.auth()
    login = firebaseAuth.sign_in_with_email_and_password(identity['email'], identity['password'])
    return login

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        resident = Resident(phone=form.phone.data, email=form.email.data)
        resident.set_password(form.password.data)
        db.session.add(resident)
        db.session.commit()
        flash('Bạn đã đăng ký thành công!')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', title='Register', form=form)

