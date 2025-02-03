from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from utils import config
from flask_migrate import Migrate


db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from app.models import models
        from app.auth import auth
        from app.admins import admins
        from app.employees import employees
        from objects.user import User

        app.config.from_object(config.Config)

        db.init_app(app)
        migrate = Migrate(app, db)
        jwt.init_app(app)
        CORS(app)

        @jwt.user_lookup_loader
        def load_user(jwt_header, jwt_payload):
            user_id = jwt_payload.get('sub')
            return User.from_user_id(user_id) if user_id else None

        app.register_blueprint(auth, url_prefix="/")
        app.register_blueprint(admins, url_prefix="/admins")
        app.register_blueprint(employees, url_prefix="/employees")

    return app
