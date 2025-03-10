# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column as Column
from marshmallow import Schema, fields
import os
from base import db, ApiFactory

# Flask uygulamasını başlat
app = Flask(__name__)

# Veritabanı yapılandırması
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy ve API Factory'yi başlat
db.init_app(app)
api_factory = ApiFactory(app)

# Model ve şemaları tanımla
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200),unique=False, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'

# class Post(db.Model):
#     __tablename__ = 'posts'
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
#     def __repr__(self):
#         return f'<Post {self.title}>'

# Şemaları tanımla
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required= True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    
# class PostSchema(Schema):
#     id = fields.Int(dump_only=True)
#     title = fields.Str(required=True)
#     content = fields.Str(required=True)
#     created_at = fields.DateTime(dump_only=True)
#     user_id = fields.Int(required=True)

# API'leri oluştur
user_schema = UserSchema()
# post_schema = PostSchema()

# Kullanıcı API'sini oluştur
user_api = api_factory.create_api(
    model=User,
    schema=user_schema,
    schema_many= UserSchema(many=True),
    url_prefix='/api/users'
)

# Post API'sini oluştur
# post_api = api_factory.create_api(
#     model=Post,
#     schema=post_schema,
#     schema_many= PostSchema(many=True),
#     url_prefix='/api/posts'
# )

# Kullanıcı postlarını getirmek için özel rota
# @user_api.register_custom_route('/<int:user_id>/posts', methods=['GET'])
# def get_user_posts(user_id):
#     user = user_api._get_item_or_404(user_id)
#     if isinstance(user, tuple):  # Eğer hata dönerse
#         return user
    
#     posts = Post.query.filter_by(user_id=user_id).all()
#     return jsonify(post_api.schema_many.dump(posts))

# Kullanıcı arama için özel rota ekle
@app.route('/api/user/search', methods=['GET'])
def search_users():
    username = request.args.get('username', '')
    users = User.query.filter(User.username.like(f'%{username}%')).all()
    return jsonify(user_api.schema_many.dump(users))

# Veritabanını oluştur
# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True,port=5002)