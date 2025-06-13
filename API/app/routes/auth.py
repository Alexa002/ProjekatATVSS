from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User, RoleEnum, UserProfile
from app import db

auth_bp = Blueprint('auth', __name__)

from datetime import datetime

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ['email', 'password', 'first_name', 'last_name', 'gender', 'birth_date']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409

    # Convert birth_date string to Python date object
    try:
        birth_date_obj = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid birth_date format, expected YYYY-MM-DD'}), 400

    user = User(
        email=data['email'],
        role=RoleEnum.USER
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()  # Commit so user.id is generated

    profile = UserProfile(
        user_id=user.id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        gender=data['gender'],
        interested_in=data.get('interested_in'),
        birth_date=birth_date_obj,
        bio=data.get('bio'),
        location=data.get('location')
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({'message': 'User and profile created successfully'}), 201



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Account is disabled'}), 403 
    
    access_token = create_access_token(identity={
        'id' : user.id,
        'email' : user.email,
        'role' : user.role.value
    })
    
    return jsonify({
        'access_token': access_token,
        'user' : {
            'id' : user.id,
            'email' : user.email,
            'role' : user.role.value
        }
    }), 200
    
    
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user() :
    current_user = get_jwt_identity()
    if not current_user:
            return jsonify({'message': 'No user identity found'}), 401
    
    user = User.query.get(current_user['id'])
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'role': user.role.value
    }), 200
    
    
