from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os

# Flaskアプリケーションの初期化
app = Flask(__name__)

# アプリケーションの設定
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key') # flaskの暗号化キー
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev_jwt_key') # JWTの暗号化キー
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pytalk.sqlite3') # データベースの接続設定
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # SQLAlchemyのモデルの変更を追跡しない
app.config['JSON_AS_ASCII'] = False  # 日本語文字化け防止

# 拡張機能の初期化
db = SQLAlchemy(app) # データベースの接続
ma = Marshmallow(app) # データベースのモデルをJSONに変換
jwt = JWTManager(app) # JWTのセットアップ
migrate = Migrate(app, db) # データベースのマイグレーション

# カスタムコマンドの登録
from src.commands import init_db_command, seed_db_command
app.cli.add_command(init_db_command)
app.cli.add_command(seed_db_command)

# Blueprintの登録（APIのルーティングの分割管理）
from src.user_api import user_bp
from src.message_api import message_bp
from src.chatroom_api import chatroom_bp

app.register_blueprint(user_bp, url_prefix='/api/user') # ユーザーAPIのルーティング
app.register_blueprint(message_bp, url_prefix='/api/message') # メッセージAPIのルーティング
app.register_blueprint(chatroom_bp, url_prefix='/api/chatroom') # チャットルームAPIのルーティング

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500