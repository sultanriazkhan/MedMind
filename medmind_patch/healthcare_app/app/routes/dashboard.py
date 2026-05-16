# app/routes/dashboard.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def dashboard_home():
    """Main dashboard view"""
    # Debug print to verify authentication
    print(f"Dashboard accessed - User authenticated: {current_user.is_authenticated}")
    print(f"User ID: {current_user.get_id() if current_user.is_authenticated else 'None'}")
    print(f"User email: {current_user.email if current_user.is_authenticated else 'None'}")
    
    return render_template('dashboard/dashboard.html', page_title='Dashboard')