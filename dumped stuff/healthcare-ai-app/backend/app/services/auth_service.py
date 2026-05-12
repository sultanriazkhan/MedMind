import jwt
import os
from datetime import datetime, timedelta
import random
import string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class AuthService:
    def generate_access_token(self, user_id):
        payload = {
            'user_id': user_id,
            'type': 'access',
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    
    def generate_refresh_token(self, user_id):
        payload = {
            'user_id': user_id,
            'type': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=30)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    
    def generate_email_verification_token(self, user_id):
        payload = {
            'user_id': user_id,
            'type': 'email_verify',
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    
    def verify_email_token(self, token):
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            if payload.get('type') == 'email_verify':
                return payload['user_id']
        except:
            return None
        return None
    
    def generate_password_reset_token(self, user_id):
        payload = {
            'user_id': user_id,
            'type': 'password_reset',
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    
    def verify_password_reset_token(self, token):
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            if payload.get('type') == 'password_reset':
                return payload['user_id']
        except:
            return None
        return None
    
    def send_verification_email(self, email, token):
        link = f"{os.getenv('FRONTEND_URL')}/verify-email?token={token}"
        message = Mail(
            from_email='noreply@healthcareai.com',
            to_emails=email,
            subject='Verify Your Email',
            html_content=f'<a href="{link}">Click here to verify your email</a>'
        )
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            sg.send(message)
        except:
            pass
    
    def send_password_reset_email(self, email, token):
        link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
        message = Mail(
            from_email='noreply@healthcareai.com',
            to_emails=email,
            subject='Reset Your Password',
            html_content=f'<a href="{link}">Click here to reset your password</a>'
        )
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            sg.send(message)
        except:
            pass