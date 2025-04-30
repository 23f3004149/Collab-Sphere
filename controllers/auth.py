from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask_login import login_user, logout_user, login_required
from models import db, User
from flask_bcrypt import Bcrypt
from datetime import timedelta

bcrypt = Bcrypt()
auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken. Choose another.', 'danger')
            return redirect(url_for('auth.register'))
        if existing_email:
            flash('Email already registered. Choose another.', 'danger')
            return redirect(url_for('auth.login'))
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password_hash=hashed_password,email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'succes')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=remember, duration=timedelta(days=30))
            session['user_id'] = user.id
            flash('Login successful!', 'succes')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'succes')
    return redirect(url_for('index'))
