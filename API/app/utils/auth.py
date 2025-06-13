from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
from app.models.user import RoleEnum

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] != RoleEnum.ADMIN.value:
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def moderator_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] != RoleEnum.MODERATOR.value:
            return jsonify({'message': 'Moderator or Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper
        

