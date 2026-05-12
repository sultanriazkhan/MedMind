# app/routes/lifestyle.py
"""Lifestyle Routes
Health profile and recommendations
"""

from flask import Blueprint, render_template
from flask_login import login_required

lifestyle_bp = Blueprint('lifestyle', __name__)


@lifestyle_bp.route('/profile')
@login_required
def health_profile():
    """Health profile setup page"""
    return render_template('lifestyle/health_profile.html', page_title='Health Profile')


@lifestyle_bp.route('/recommendations')
@login_required
def recommendations():
    """Lifestyle recommendations dashboard"""
    return render_template('lifestyle/recommendations.html', page_title='Recommendations')


@lifestyle_bp.route('/diet')
@login_required
def diet():
    """Diet recommendations page"""
    return render_template('lifestyle/diet.html', page_title='Diet Plan')


@lifestyle_bp.route('/exercise')
@login_required
def exercise():
    """Exercise recommendations page"""
    return render_template('lifestyle/exercise.html', page_title='Exercise Plan')