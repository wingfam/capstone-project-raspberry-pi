from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.firebase_config import firebaseApp, firebaseDB, identity
from app.models import Resident, System
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.auth.email import send_password_reset_email
from werkzeug.urls import url_parse

# @bp.route('/login', methods=['GET', 'POST'])
# def login():
    # Redirect to index if user have already logged in
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     resident = Resident.query.filter_by(phone=form.phone.data).first()
    #     if resident is None or not resident.check_password(form.password.data):
    #         flash('Invalid phone number or password')
    #         return redirect(url_for('auth.login'))
        
    #     login_user(resident, remember=form.remember_me.data)
        
    #     next_page = request.args.get('next')
    #     if not next_page or url_parse(next_page).netloc != '':
    #         next_page = url_for('main.index')
    #     return redirect(next_page)
    # return render_template('auth/login.html', title='Sign In', form=form)

# @bp.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('main.index'))

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

# @bp.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         resident = Resident.query.filter_by(email=form.email.data).first()
#         if resident:
#             send_password_reset_email(resident)
#         flash('Check your email for the instructions to reset your password')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password_request.html',
#                            title='Reset Password', form=form)


# @bp.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     resident = Resident.verify_reset_password_token(token)
#     if not resident:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         resident.set_password(form.password.data)
#         db.session.commit()
#         flash('Your password has been reset.')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password.html', form=form)
