# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    # If already logged in, redirect to dashboard
    if current_user.is_authenticated:
        print("User already authenticated, redirecting to dashboard")
        return redirect(url_for('dashboard.dashboard_home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        print(f"Login attempt - Email: {email}, Remember: {remember}")
        
        # Demo: Accept any credentials
        user = User.get_by_email(email)
        if not user:
            user = User.create(email, password, email.split('@')[0])
        
        # CRITICAL: Call login_user() to create session
        login_user(user, remember=remember)
        
        # Verify session was created
        print(f"After login_user - Current user: {current_user.is_authenticated}, ID: {current_user.get_id() if current_user.is_authenticated else 'None'}")
        
        flash('Login successful! Welcome back.', 'success')
        
        # Get next page from request args
        next_page = request.args.get('next')
        print(f"Next page: {next_page}")
        
        if next_page:
            return redirect(next_page)
        return redirect(url_for('dashboard.dashboard_home'))
    
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"Signup - Name: {name}, Email: {email}")
        
        # Create user
        user = User.create(email, password, name)
        
        # CRITICAL: Call login_user() to create session
        login_user(user)
        
        print(f"After signup - User authenticated: {current_user.is_authenticated}")
        
        flash('Account created successfully! Welcome to HealthAI.', 'success')
        return redirect(url_for('dashboard.dashboard_home'))
    
    return render_template('auth/signup.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password reset request page"""
    if request.method == 'POST':
        email = request.form.get('email')
        flash('Password reset instructions sent to your email.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))