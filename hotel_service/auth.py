# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import Account
from . import db, login_manager

auth = Blueprint('auth', __name__)

@login_manager.unauthorized_handler
def unauthorized():
    flash('You are not authorized to view that page. Please login.')
    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember-me') else False
    
    user = Account.query.filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    
    # if this returns a user, then the email already exists in database
    username_unavail = Account.query.filter_by(username=username).first() is not None
    email_unavail = Account.query.filter_by(email=email).first() is not None
    if username_unavail and email_unavail:
        flash_msg = []
        if email_unavail:
            flash_msg.append('Email address')
        if username_unavail:
            flash_msg.append('Username')
        
        flash(' and '.join(flash_msg) + ' already exists')
        return redirect(url_for('auth.signup'))
    
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = Account(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password=generate_password_hash(password, method='sha256'),
    )
    
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))