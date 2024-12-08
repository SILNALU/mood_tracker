from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db
from functools import wraps
import re

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def is_valid_password(password):
    """
    Validate password strength
    Requirements:
    - At least 8 characters long
    - Contains at least one digit
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    if request.method == 'POST':
        # Ensure username was submitted
        if not request.form.get('username'):
            flash('Must provide username', 'error')
            return render_template('auth/login.html'), 403

        # Ensure password was submitted
        elif not request.form.get('password'):
            flash('Must provide password', 'error')
            return render_template('auth/login.html'), 403

        # Query database for username
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', 
            (request.form.get('username'),)
        ).fetchone()

        # Ensure username exists and password is correct
        if user is None:
            flash('Invalid username', 'error')
            return render_template('auth/login.html'), 403
        
        if not check_password_hash(user['password'], request.form.get('password')):
            flash('Invalid password', 'error')
            return render_template('auth/login.html'), 403

        # Remember which user has logged in
        session['user_id'] = user['id']
        session.permanent = True  # Make session persistent

        # Redirect user to home page
        flash('Logged in successfully!', 'success')
        return redirect(url_for('mood.select_mood'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register user"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # Ensure username was submitted
        if not username:
            flash('Must provide username', 'error')
            return render_template('auth/register.html'), 400

        # Username length validation
        if len(username) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return render_template('auth/register.html'), 400

        # Username character validation
        if not username.isalnum():
            flash('Username must contain only letters and numbers', 'error')
            return render_template('auth/register.html'), 400

        # Ensure password was submitted
        if not password:
            flash('Must provide password', 'error')
            return render_template('auth/register.html'), 400

        # Validate password strength
        is_valid, message = is_valid_password(password)
        if not is_valid:
            flash(message, 'error')
            return render_template('auth/register.html'), 400

        # Ensure confirmation was submitted
        if not confirmation:
            flash('Must confirm password', 'error')
            return render_template('auth/register.html'), 400

        # Ensure passwords match
        if password != confirmation:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html'), 400

        try:
            db = get_db()
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            
            # Get the user that was just created
            user = db.execute(
                'SELECT * FROM users WHERE username = ?', (username,)
            ).fetchone()
            
            # Log the user in
            session['user_id'] = user['id']
            session.permanent = True  # Make session persistent
            flash('Registered successfully!', 'success')
            return redirect(url_for('mood.select_mood'))
            
        except db.IntegrityError:
            flash('Username already exists', 'error')
            return render_template('auth/register.html'), 400

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    """Log user out"""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))