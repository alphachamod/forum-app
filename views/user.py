# views/user.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models import User, db
from helpers.security_helper import SecurityHelper  # Import SecurityHelper
from functools import wraps

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You must be logged in to view this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('forum.forum'))  # Redirect to forum
    return render_template('user/profile.html', user=user)


@user_bp.route('/edit', methods=['GET', 'POST'])
@login_required  # Requires the user to be logged in to access this
def edit_profile():
    user = User.query.filter_by(username=session['username']).first() # Get user
    # Get user from db
    if request.method == 'POST':
        # Retrieve form values
        new_email = request.form['email'] #Get value
        new_password = request.form['password']

        # Insecure implementation to store password hash
        new_hashed_password = SecurityHelper.hash_password(new_password)

        #Assign the database to the new values
        user.email = new_email
        user.password_hash = new_hashed_password

        # Commit and push to database
        db.session.commit()

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user.profile', username=user.username))
    return render_template('user/edit_profile.html', user=user) # Directs the users to the edit profile