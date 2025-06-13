# routes/messages.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Conversation, Message, User
from datetime import datetime
from app import db

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    current_user_id = get_jwt_identity()["id"]
    
    conversations = Conversation.query.filter(
        (Conversation.user1_id == current_user_id) |
        (Conversation.user2_id == current_user_id)
    ).order_by(Conversation.updated_at.desc()).all()
    
    result = []
    for conv in conversations:
        other_user = conv.user2 if conv.user1_id == current_user_id else conv.user1
        last_message = Message.query.filter_by(conversation_id=conv.id).order_by(Message.sent_at.desc()).first()
        
        result.append({
            "conversation_id": conv.id,
            "other_user": {
                "id": other_user.id,
                "name": f"{other_user.profile.first_name} {other_user.profile.last_name}",
                "avatar": other_user.photos[0].photo_url if other_user.photos else None
            },
            "last_message": {
                "content": last_message.content if last_message else None,
                "sent_at": last_message.sent_at.isoformat() if last_message else None,
                "is_read": last_message.is_read if last_message else True
            },
            "unread_count": Message.query.filter_by(
                conversation_id=conv.id,
                is_read=False
            ).filter(Message.sender_id != current_user_id).count()
        })
    
    return jsonify(conversations=result)

@messages_bp.route('/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    current_user_id = get_jwt_identity()["id"]
    
    conversation = Conversation.query.get_or_404(conversation_id)
    if current_user_id not in [conversation.user1_id, conversation.user2_id]:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Mark messages as read
    Message.query.filter_by(
        conversation_id=conversation_id,
        is_read=False
    ).filter(Message.sender_id != current_user_id).update({"is_read": True})
    db.session.commit()
    
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.sent_at.asc()).all()
    
    return jsonify(messages=[{
        "id": msg.id,
        "content": msg.content,
        "sender_id": msg.sender_id,
        "sent_at": msg.sent_at.isoformat(),
        "is_read": msg.is_read
    } for msg in messages])

@messages_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = get_jwt_identity()["id"]
    data = request.get_json()
    
    # Find or create conversation
    user1_id, user2_id = sorted([current_user_id, data['recipient_id']])
    conversation = Conversation.query.filter_by(
        user1_id=user1_id,
        user2_id=user2_id
    ).first()
    
    if not conversation:
        conversation = Conversation(user1_id=user1_id, user2_id=user2_id)
        db.session.add(conversation)
        db.session.commit()
    
    # Create message
    message = Message(
        conversation_id=conversation.id,
        sender_id=current_user_id,
        content=data['content']
    )
    db.session.add(message)
    conversation.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(message={
        "id": message.id,
        "content": message.content,
        "sender_id": message.sender_id,
        "sent_at": message.sent_at.isoformat(),
        "is_read": message.is_read
    }), 201