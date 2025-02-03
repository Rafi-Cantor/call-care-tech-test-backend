from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_current_user
from app.auth import auth
from objects.user import User, UserAlreadyExistsError
from functools import wraps


def user_type(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if "employee" in required_roles and user.is_admin:
                return jsonify({"msg": "Forbidden: Admins cannot access employee routes"}), 403
            if "admin" in required_roles and not user.is_admin:
                return jsonify({"msg": "Forbidden: Admin permissions required"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")
    user = User.from_user_name(user_name)
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.user_id)
        return jsonify({
            "access_token": access_token,
            "user_id": user.user_id,
            "user_name": user.user_name,
            "is_admin": user.is_admin,
        }), 200
    return jsonify({"msg": "Invalid credentials"}), 401


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")
    is_admin = data.get("is_admin", False)
    try:
        user = User.create(user_name, is_admin, password)
    except UserAlreadyExistsError as e:
        print(e)
        return jsonify({"msg": f"Failed: {e}"}), 400
    access_token = create_access_token(identity=str(user.user_id))
    return jsonify({
        "access_token": access_token,
        "user_id": user.user_id,
        "user_name": user.user_name,
        "is_admin": user.is_admin
    }), 201
