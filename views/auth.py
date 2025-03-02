# views/auth.py
# Import the session from flask to handle session values.
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models import User, db  # Import models and the database instance
from werkzeug.security import generate_password_hash, check_password_hash  # Insecure password hashing
from helpers.security_helper import SecurityHelper

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Get password
        email = request.form['email']

        # Insecure Password Hashing (MD5)
        # hashed_password = generate_password_hash(password) # VULNERABLE replace to hash
        hashed_password = SecurityHelper.hash_password(password)

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')

        # Insecure: no CSRF
        new_user = User(username=username, password_hash=hashed_password, email=email)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Insecure: SQL Injection!
        # query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
        # user = db.session.execute(query).fetchone()
        user = User.query.filter_by(username=username).first()
        # user = User.query.filter(User.username.like('what%')).all()
        if not user:
            flash('Invalid username.', 'error')
            return render_template('login.html')

        isCorrectPassword = user.check_password(password)  # VULNERABLE

        if user and isCorrectPassword:
            # Use the session to store the user's username during login
            session['username'] = user.username # Create a session variable

            flash('Login successful!', 'success')
            return redirect(url_for('forum.forum'))  # Redirect user
        else:
            flash('Invalid password.', 'error')
            return render_template('login.html')
    return render_template('login.html')

# Logout authentication from session
@auth_bp.route('/logout')
def logout():
    session.pop('username', None) #delete session variables
    flash("Logged out!", "success")
    return redirect(url_for('auth.login')) #redirect to login page