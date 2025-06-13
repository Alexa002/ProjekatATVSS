from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User, RoleEnum
from app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = User.query.get(get_jwt_identity()['id'])
    if not current_user.is_admin():
        return jsonify({'message':'Admin access required'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.paginate(page = page, per_page = per_page, error_out = False)
    
    user_list = []
    for user in users.items:
        user_list.append({
            'id': user.id,
            'email': user.email,
            'role': user.role.value,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        })
        
    return jsonify({
        'users': user_list,
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    }), 200
    
    
@admin_bp.route('/users/<int:user_id>/role',  methods=['PUT'])
@jwt_required()
def update_user_roles(user_id):
    current_user = User.query.get_or_404(get_jwt_identity()['id'])
    if not current_user.is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    if 'role' not in data:
        return jsonify({'message': 'Role is required'}), 400
    
    try:
        new_role = RoleEnum(data['role'])
    except ValueError:
        return jsonify({'message': 'Invalid role'}), 400
    
    
    user = User.query.get_or_404(user_id)
    user.role = new_role
    db.session.commit()
    
    return jsonify({'message': 'User role updated successfully'}), 200


    