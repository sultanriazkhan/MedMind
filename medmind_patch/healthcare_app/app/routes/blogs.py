# app/routes/blogs.py
"""Blog Routes
Health articles and blog content
"""

from flask import Blueprint, render_template, request
from flask_login import login_required

blogs_bp = Blueprint('blogs', __name__)


@blogs_bp.route('/')
@login_required
def blog_listing():
    """Blog listing page"""
    return render_template('blogs/blog_listing.html', page_title='Health Blog')


@blogs_bp.route('/post/<int:post_id>')
@login_required
def blog_reading(post_id):
    """Individual blog post reading page"""
    return render_template('blogs/blog_reading.html', page_title='Read Article', post_id=post_id)


@blogs_bp.route('/search')
@login_required
def blog_search():
    """Blog search results page"""
    query = request.args.get('q', '')
    return render_template('blogs/blog_search.html', page_title='Search Results', search_query=query)