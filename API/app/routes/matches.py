from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..models import Match, User

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/matched', methods=['GET'])
@jwt_required()
def get_my_matches():
    try:
        current_user_id = get_jwt_identity()["id"]
        
        matches = Match.query.filter(
            (Match.user1_id == current_user_id) | 
            (Match.user2_id == current_user_id)
        ).all()

        matches_data = []
        for match in matches:
            other_user = match.user2 if match.user1_id == current_user_id else match.user1
            
            # Get primary photo if exists
            primary_photo = next(
                (photo.photo_url for photo in other_user.photos if photo.is_primary),
                None
            )
            
            profile_data = {}
            if other_user.profile:
                profile_data = {
                    "first_name": other_user.profile.first_name,
                    "last_name": other_user.profile.last_name,
                    "full_name": f"{other_user.profile.first_name} {other_user.profile.last_name}",
                    "age": other_user.profile.age(),
                    "gender": other_user.profile.gender,
                    "interested_in": other_user.profile.interested_in,
                    "bio": other_user.profile.bio,
                    "location": other_user.profile.location,
                    "profile_picture": primary_photo
                }

            matches_data.append({
                "match_id": match.id,
                "matched_at": match.matched_at.isoformat(),
                "user": {
                    "id": other_user.id,
                    "email": other_user.email,
                    "role": other_user.role.value
                },
                "profile": profile_data
            })

        return jsonify({
            "success": True,
            "matches": matches_data,
            "count": len(matches_data)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500