from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema
from typing import Type, Dict, Any, List, Optional, Tuple, Union

db = SQLAlchemy()

class BaseModelCRUD:
    """
    Generic base class for all CRUD operations for any SQLAlchemy model.
    This class should be extended when creating API endpoints for a specific model.
    """
    
    def __init__(
        self, 
        model: db.Model, 
        schema: Schema, 
        schema_many: Schema,
        blueprint_name: str, 
        url_prefix: str,
        pk_field: str = 'id'
    ):
        """
        Initialize the BaseModelCRUD class.
        
        Args:
            model: SQLAlchemy model class
            schema: Marshmallow schema for serialization/deserialization
            blueprint_name: Name for the Flask blueprint
            url_prefix: URL prefix for all routes 
            pk_field: Primary key field name (default: 'id')
        """
        self.model = model
        self.schema = schema
        self.schema_many = schema_many
        self.blueprint_name = blueprint_name
        self.url_prefix = url_prefix
        self.pk_field = pk_field
        self.blueprint = self._create_blueprint()
    
    def _create_blueprint(self) -> Blueprint:
        """Create Flask blueprint with all CRUD routes."""
        bp = Blueprint(self.blueprint_name, __name__, url_prefix=self.url_prefix)
        
        # Register all routes
        bp.route('/', methods=['GET'])(self.get_all)
        bp.route('/<int:item_id>', methods=['GET'])(self.get_one)
        bp.route('/', methods=['POST'])(self.create)
        bp.route('/<int:item_id>', methods=['PUT'])(self.update)
        bp.route('/<int:item_id>', methods=['DELETE'])(self.delete)
        
        return bp
    
    def get_all(self) -> Tuple[Dict[str, List[Dict[str, Any]]], int]:
        """Get all records of the model."""
        items = self.model.query.all()
        return jsonify(self.schema_many.dump(items)), 200
    
    def get_one(self, item_id: int) -> Tuple[Dict[str, Any], int]:
        """Get one record by id."""
        item = self._get_item_or_404(item_id)
        return jsonify(self.schema.dump(item)), 200
    
    def create(self) -> Tuple[Dict[str, Any], int]:
        """Create a new record."""
        json_data = request.get_json()
        
        # Validate data
        errors = self.schema.validate(json_data)
        if errors:
            return jsonify({"errors": errors}), 400
        
        # Create and save new instance
        new_item = self.model(**json_data)
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify(self.schema.dump(new_item)), 201
    
    def update(self, item_id: int) -> Tuple[Dict[str, Any], int]:
        """Update an existing record."""
        item = self._get_item_or_404(item_id)
        json_data = request.get_json()
        
        # Update model fields based on data received
        for key, value in json_data.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        db.session.commit()
        return jsonify(self.schema.dump(item)), 200
    
    def delete(self, item_id: int) -> Tuple[Dict[str, Any], int]:
        """Delete a record."""
        item = self._get_item_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({"message": f"{self.model.__name__} deleted successfully"}), 200
    
    def _get_item_or_404(self, item_id: int) -> db.Model:
        """Helper method to get item or return 404 response."""
        filter_args = {self.pk_field: item_id}
        item = self.model.query.filter_by(**filter_args).first()
        
        if item is None:
            # Flask'ın abort fonksiyonunu kullanmak yerine özel 404 hatası döndür
            response = jsonify({"error": f"{self.model.__name__} not found"})
            response.status_code = 404
            return response
        
        return item
    
    def register_custom_route(
        self,
        rule: str, 
        endpoint: Optional[str] = None, 
        methods: List[str] = None,
        
        **options
        
    ):
        """Register a custom route on the blueprint."""
        # @wraps(f)
        def decorator(f):
            self.blueprint.add_url_rule(rule, endpoint, f, methods=methods, **options)
            return f
        return decorator


class ApiFactory:
    """
    Factory class to simplify the creation of API endpoints for models.
    """
    
    def __init__(self, app: Flask = None):
        """
        Initialize the API factory.
        
        Args:
            app: Flask application instance
        """
        self.app = app
        self.blueprints = []
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """
        Initialize the API factory with a Flask application.
        
        Args:
            app: Flask application instance
        """
        self.app = app
        
        # Register all previously created blueprints
        for bp in self.blueprints:
            app.register_blueprint(bp)
    
    def create_api(
        self, 
        model: db.Model, 
        schema: Schema,
        schema_many:Schema, 
        url_prefix: str, 
        blueprint_name: Optional[str] = None,
        pk_field: str = 'id'
    ) -> BaseModelCRUD:
        """
        Create a new API for a model.
        
        Args:
            model: SQLAlchemy model class
            schema: Marshmallow schema for the model
            url_prefix: URL prefix for all routes 
            blueprint_name: Optional blueprint name (defaults to model name)
            pk_field: Primary key field name (default: 'id')
            
        Returns:
            BaseModelCRUD instance
        """
        if blueprint_name is None:
            blueprint_name = model.__name__.lower()
        
        api = BaseModelCRUD(
            model=model,
            schema=schema,
            schema_many=schema_many,
            blueprint_name=blueprint_name,
            url_prefix=url_prefix,
            pk_field=pk_field
        )
        
        if self.app:
            self.app.register_blueprint(api.blueprint)
        
        self.blueprints.append(api.blueprint)
        return api


# Örnek kullanım: app.py içinde bu kodu kullanabilirsiniz
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import os
from api_base import db, ApiFactory

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
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<User {self.username}>'

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)

# API'leri oluştur
user_schema = UserSchema()
user_api = api_factory.create_api(
    model=User,
    schema=user_schema,
    url_prefix='/api/users'
)

# Özel rotalar eklemek isterseniz
@user_api.register_custom_route('/search', methods=['GET'])
def search_users():
    username = request.args.get('username', '')
    users = User.query.filter(User.username.like(f'%{username}%')).all()
    return jsonify(user_api.schema_many.dump(users))

# Veritabanını oluştur
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
"""