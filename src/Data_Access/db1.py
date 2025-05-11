# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column as Column
# from marshmallow import Schema, fields
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

from Controllers import UserController
userController = UserController.UserController(app)

# Veritabanını oluştur
# with app.app_context():
#      db.create_all()

if __name__ == '__main__':
    # app.run(debug=True,port=5002)
    app.run(host='0.0.0.0', port=5002)