# app/routes/home.py
"""Home Routes
Handles landing page and root redirects
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    """Root route - redirects to login if not authenticated, else dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_home'))
    return redirect(url_for('auth.login'))


@home_bp.route('/home')
@login_required
def landing():
    """Landing page for authenticated users"""
    return render_template('home/landing.html')