# app/routes/user.py
"""User Routes
User profile and settings management
"""

from flask import Blueprint, render_template
from flask_login import login_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('user/profile.html', page_title='My Profile')


@user_bp.route('/settings')
@login_required
def settings():
    """User settings page"""
    return render_template('user/settings.html', page_title='Settings')