# main.py
from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db, Account, HotelRoom


DATE_FORMAT = '%m-%d-%Y'

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    listings = HotelRoom.query.all()
    return render_template('index.html', listings=listings)

@main.route('/profile')
@login_required
def profile():
    listings = HotelRoom.query.filter_by(reserved_by=current_user.username).all()
    return render_template('profile.html', current_user=current_user, listings=listings)

@main.route('/listing/<id>')
@login_required
def listing(id):
    item = HotelRoom.query.get(id)
    if not item:
        flash("No listing item found.", "error")
    
    return render_template('item.html', item=item, current_user=current_user)

@main.route('/listing/<id>/reserve/<checkin>/<checkout>')
@login_required
def reserve(id, checkin, checkout):
    item = HotelRoom.query.get(id)
    if item:
        item.check_in = datetime.strptime(checkin, DATE_FORMAT)
        item.check_out = datetime.strptime(checkout, DATE_FORMAT)
        item.reserved_by = current_user.username
        item.reserved = True
        
        db.session.commit()
        flash("Successfully Reserved.", "message")
    else:
        flash("No listing item found. Failed to unreserve.", "error")
    
    return redirect(url_for('main.listing', id=id))

@main.route('/listing/<id>/unreserve')
@login_required
def unreserve(id):
    item = HotelRoom.query.get(id)
    if item:
        item.check_in = None
        item.check_out = None
        item.reserved_by = None
        item.reserved = False
        
        db.session.commit()
        flash("Successfully Unreserved.", "message")
    else:
        flash("No listing item found. Failed to unreserve.")
    
    return redirect(url_for('main.listing', id=id))
