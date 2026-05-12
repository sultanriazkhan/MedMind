# app/routes/reports.py
"""Lab Reports Routes
Handles report upload, processing, and analysis
"""

from flask import Blueprint, render_template
from flask_login import login_required

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/upload')
@login_required
def upload_report():
    """Upload lab report page"""
    return render_template('reports/upload_report.html', page_title='Upload Report')


@reports_bp.route('/processing')
@login_required
def processing():
    """Report processing screen"""
    return render_template('reports/processing.html', page_title='Processing Report')


@reports_bp.route('/analysis')
@login_required
def analysis_overview():
    """Report analysis overview"""
    return render_template('reports/analysis_overview.html', page_title='Analysis Overview')


@reports_bp.route('/explanation/<int:test_id>')
@login_required
def test_explanation(test_id):
    """Detailed test explanation"""
    return render_template('reports/test_explanation.html', page_title='Test Explanation', test_id=test_id)


@reports_bp.route('/history')
@login_required
def report_history():
    """Report history page"""
    return render_template('reports/report_history.html', page_title='Report History')