# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column as Column
from marshmallow import Schema, fields
import os
from base import db, ApiFactory

# api_factory = ApiFactory(app)

# Model ve şemaları tanımla
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200),unique=False, nullable = False)
    email = db.Column(db.String(120), unique=True)
    google_id = db.Column(db.String(),unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'



# Şemaları tanımla
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required= False)
    google_id = fields.Str(required=False)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)


# app = Flask(__name__)
class UserController():
    

    def __init__(self,app):
        self._user_schema = UserSchema()
        self._api_factory = ApiFactory(app)
        self._user_api = self._api_factory.create_api(
            model=User,
            schema=self._user_schema,
            schema_many= UserSchema(many=True),
            url_prefix='/api/users'
            )
        # @self._user_api.register_custom_route('search', methods=['GET'])
        @app.route('/api/users/search', methods=['GET'])
        def search_users():
            username = request.args.get('username', '')
            users = User.query.filter(User.username.like(f'%{username}%')).all()
            return jsonify(self._user_api.schema_many.dump(users))
        '''TODO: Make an moduler structure for all entity parameters and added to base'''
        @app.route('/api/users/mailsearch', methods=['GET'])
        def search_users_mail():
            email = request.args.get('email','')
            
            users = User.query.filter(User.email.like(f'%{email}%')).all()
            print(users)
            return jsonify(self._user_api.schema_many.dump(users))
        
    # def getapi(self):
    #     return self._user_api
    
   

   
        

# API'leri oluştur
# user_schema = UserSchema()

# # Kullanıcı API'sini oluştur
# user_api = api_factory.create_api(
#     model=User,
#     schema=user_schema,
#     schema_many= UserSchema(many=True),
#     url_prefix='/api/users'
# )


# # Kullanıcı arama için özel rota ekle
# @app.route('/api/user/search', methods=['GET'])
# def search_users():
#     username = request.args.get('username', '')
#     users = User.query.filter(User.username.like(f'%{username}%')).all()
#     return jsonify(user_api.schema_many.dump(users))

# Veritabanını oluştur
# with app.app_context():
#     db.create_all()