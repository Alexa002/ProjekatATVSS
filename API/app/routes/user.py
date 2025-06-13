
from ..config import cloudinary
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User, UserProfile, UserPhoto
from app.models.message import Conversation, Message
from app import db
from datetime import datetime
from app.models.match import Like, Match



user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()['id']
    user = User.query.get_or_404(current_user_id)
    
    if request.method == 'GET' :
        profile = user.profile
        profile_data = {}
        
        if profile:
            profile_data = {
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'gender': profile.gender,
                'interested_in': profile.interested_in,
                'birth_date': profile.birth_date.isoformat() if profile.birth_date else None,
                'bio': profile.bio,
                'location': profile.location,
                'age': profile.age() if profile.birth_date else None,    
            }
        
        photos = [{'id': p.id, 'url': p.photo_url, 'is_primary': p.is_primary} for p in user.photos]
        
        return jsonify({
            'email': user.email,
            'profile': profile_data,
            'photos': photos,
        }), 200
        
    elif request.method == 'PUT':
        data = request.get_json()
        
        if not user.profile:
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)
        else:
            profile = user.profile
            
        profile.first_name = data.get('first_name', profile.first_name)
        profile.last_name = data.get('last_name', profile.last_name)
        profile.gender = data.get('gender', profile.gender)
        profile.interested_in = data.get('interested_in', profile.interested_in)
       
        if 'birth_date' in data:
            profile.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
       
        profile.bio = data.get('bio', profile.bio)
        profile.location = data.get('location', profile.location)        
        
        
        db.session.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
    
@user_bp.route('/photos', methods=['POST'])
@jwt_required()
def upload_photo():
    current_user_id = get_jwt_identity()['id']
    user = User.query.get_or_404(current_user_id)
    
    if 'photo' not in request.files:
        return jsonify({'message' : 'No photo uploaded'}), 400
    
    photo_file = request.files['photo']
    
    try:
        upload_result = cloudinary.uploader.upload(photo_file,folder=f"user_{current_user_id}/photos")  
    except Exception as e:
        return jsonify({'message': 'Photo upload failed', 'error': str(e)}), 500
    
    photo_url = upload_result['secure_url']
    
    new_photo = UserPhoto(
        
        user_id = user.id,
        photo_url = photo_url,
        is_primary = False
    )
    
    db.session.add(new_photo)
    db.session.commit()
    
    return jsonify({
        'message': 'Photo uploaded successfully',
        'photo': {
            'id': new_photo.id,
            'url': new_photo.photo_url,
            'is_primary': new_photo.is_primary
        }
    }), 201


@user_bp.route('/photos/<int:photo_id>/primary', methods=['PUT'])
@jwt_required()
def set_primary_photo(photo_id):
    current_user_id = get_jwt_identity()['id']
    photo = UserPhoto.query.filter_by(id = photo_id, user_id = current_user_id).first_or_404()
    
    UserPhoto.query.filter_by(user_id = current_user_id).update({'is_primary': False})
    
    photo.is_primary = True
    db.session.commit()
    
    return jsonify({'message' : 'Primry photo updated successfully'}), 200


@user_bp.route('/photos/<int:photo_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_photo(photo_id):
    current_user_id = get_jwt_identity()['id']
    try:
       
        photo = UserPhoto.query.get(photo_id)
        
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
       
        is_primary = photo.is_primary
        
        
        db.session.delete(photo)
        db.session.commit()
        
       
        if is_primary:
            
            new_primary = UserPhoto.query.filter(
                UserPhoto.user_id == photo.user_id,
                UserPhoto.id != photo_id
            ).first()
            
            if new_primary:
                new_primary.is_primary = True
                db.session.commit()
        
        cloudinary.uploader.destroy(photo.photo_url)
       
        return jsonify({'message': 'Photo deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@user_bp.route('/discover', methods=['GET'])
@jwt_required()
def discover_users():
    current_user_id = get_jwt_identity()['id']
    current_user = User.query.get_or_404(current_user_id)
    
    interested_in = current_user.profile.interested_in
    gender_filter = 'male' if interested_in == 'female' else 'female' if interested_in == 'male' else None
    
    query = User.query.join(UserProfile).filter(
        User.id != current_user_id,
        User.is_active == True
    )
    
    if gender_filter:
        query = query.filter(UserProfile.gender == gender_filter)
        
        
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_users = query.paginate(page = page, per_page = per_page, error_out = False)
    
    users = []
    for user in paginated_users.items:
        primary_photo = next((p for p in user.photos if p.is_primary), None)
        users.append({
            'id': user.id,
            'first_name': user.profile.first_name,
            'age': user.profile.age(),
            'bio': user.profile.bio,
            'location': user.profile.location,
            'photo': primary_photo.photo_url if primary_photo else None
        })
        
    return jsonify({
        'users' : users,
        'total' : paginated_users.total,
        'pages' : paginated_users.pages,
        'current_page' : paginated_users.page
    }), 200
    
    
@user_bp.route('/like/<int:user_id>', methods=['POST'])
@jwt_required()
def like_user(user_id):
    current_user_id = get_jwt_identity()['id']
    
    if current_user_id == user_id:
        return jsonify({'message': 'Cannot like yourself'}), 400
    
    
    target_user = User.query.get_or_404(user_id)
    
    existing_like = Like.query.filter_by(liker_id = current_user_id, liked_id = user_id ).first()
    if existing_like:
        return jsonify({'message': 'Already liked this user'}), 400

    their_like = Like.query.filter_by(liker_id = user_id, liked_id = current_user_id).first()
    
    new_like = Like(liker_id = current_user_id, liked_id = user_id)
    db.session.add(new_like)
    
    if their_like:
        new_match = Match(user1_id=min(current_user_id, user_id), 
                         user2_id=max(current_user_id, user_id))
        db.session.add(new_match)
        db.session.commit()
        
        return jsonify({
            'message': 'It\'s a match!',
            'match': True,
            'user': {
                'id': target_user.id,
                'name': f"{target_user.profile.first_name} {target_user.profile.last_name}"
            }
        }), 201
    else:
        db.session.commit()
        return jsonify({'message': 'Like recorded', 'match': False}), 201
        