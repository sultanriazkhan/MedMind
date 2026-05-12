# app/routes/auth.py
"""Authentication Routes
Handles login, signup, and password reset functionality
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Demo mode - accept any credentials
        flash('Demo mode: Logged in successfully!', 'success')
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
        
        flash('Demo mode: Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/signup.html')


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password reset request page"""
    if request.method == 'POST':
        email = request.form.get('email')
        flash('Demo mode: Password reset link sent to your email!', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/forgot_password.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))