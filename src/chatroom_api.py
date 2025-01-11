from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src import db
from src.db import ChatRoom

chatroom_bp = Blueprint('chatroom', __name__)

@chatroom_bp.route('/', methods=['POST'])
@jwt_required()
def create_chatroom():
    data = request.get_json()
    
    new_chatroom = ChatRoom(
        name=data['name'],
        is_private=data.get('is_private', False)
    )
    
    try:
        db.session.add(new_chatroom)
        db.session.commit()
        return jsonify({'message': 'Chat room created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500