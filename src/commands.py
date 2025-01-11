import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from src import db
from src.db import User

@click.command('init-db')
@with_appcontext
def init_db_command():
    """データベースの初期化とテーブルの作成"""
    db.create_all()
    click.echo('データベースを初期化しました。')
    
@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """テストデータの追加"""
    test_user = User(
        username='test_user',
        email='test@example.com',
        password=generate_password_hash('password123')
    )
    db.session.add(test_user)
    db.session.commit()
    click.echo('テストデータを追加しました。')
