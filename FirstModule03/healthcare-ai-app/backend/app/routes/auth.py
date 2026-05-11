from flask import Blueprint, request, jsonify, make_response
from app.models.user import User
from app import db
from datetime import datetime
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        full_name=data['full_name'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'user': user.to_dict(),
        'access_token': 'dummy_token_for_now'
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({
        'user': user.to_dict(),
        'access_token': 'dummy_token_for_now'
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logged out successfully'}))
    return response

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    return jsonify({'id': 1, 'full_name': 'Test User', 'email': 'test@example.com'})