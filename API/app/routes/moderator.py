from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app import db

moderator_bp = Blueprint('moderator', __name__)

@moderator_bp.route('/users/<int:user_id>/suspend', methods=['POST'])
@jwt_required()
def suspend_user(user_id):
    current_user = User.query.get(get_jwt_identity()['id'])
    if not current_user.is_moderator() and not current_user.is_admin():
        return jsonify({'message': 'Moderator access required'}), 403
    
    user = User.query.get_or_404(user_id)
    
    if user.is_admin():
        return jsonify({'message': 'Cannot suspend an admin'}), 403
    
    user.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'User suspended successfully'}), 200

@moderator_bp.route('/users/<int:user_id>/unsuspend', methods=['POST'])
@jwt_required()
def unsuspend_user(user_id):
    current_user = User.query.get(get_jwt_identity()['id'])
    if not current_user.is_moderator() and not current_user.is_admin():
        return jsonify({'message': 'Moderator access required'}), 403
    
    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    
    return jsonify({'message': 'User unsuspended successfully'}), 200