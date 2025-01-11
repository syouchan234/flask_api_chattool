from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src import db
from src.db import Message

message_bp = Blueprint('message', __name__)

@message_bp.route('/', methods=['POST'])
@jwt_required()
def create_message():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    new_message = Message(
        content=data['content'],
        user_id=user_id,
        chat_room_id=data['chat_room_id']
    )
    
    try:
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500