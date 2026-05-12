# app/models.py
from flask_login import UserMixin

class User(UserMixin):
    """User model for Flask-Login"""
    
    def __init__(self, id, email, name):
        self.id = str(id)  # Must be string
        self.email = email
        self.name = name
        # These are properties from UserMixin, don't set them directly
        # They default to True automatically
    
    def get_id(self):
        """Required by Flask-Login"""
        return self.id
    
    @property
    def is_active(self):
        """Override if you want to deactivate users"""
        return True
    
    @property
    def is_authenticated(self):
        """Override if needed"""
        return True
    
    @property
    def is_anonymous(self):
        """Override if needed"""
        return False
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID - CRITICAL for Flask-Login"""
        print(f"Getting user by ID: {user_id}")
        if user_id == '1' or user_id == 1:
            return User(id='1', email='demo@healthai.com', name='Demo User')
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        print(f"Getting user by email: {email}")
        if email:
            return User(id='1', email=email, name=email.split('@')[0])
        return None
    
    @staticmethod
    def create(email, password, name):
        """Create new user (demo)"""
        print(f"Creating user: {email}, {name}")
        return User(id='1', email=email, name=name)