from flask_jwt_extended import jwt_required, get_current_user
from flask import jsonify, request
from app.admins import admins
from objects import user, level
from app.auth import routes


@admins.route("/all_employees", methods=["GET"])
@jwt_required()
@routes.user_type(["admin"])
def get_all_employees():
    e = user.User.all_employees()
    employee_data = [
        {
            "user_id": employee.user_id,
            "user_name": employee.user_name,
            "xp": employee.xp, "level_id": employee.current_level_id
        } for employee in e
    ]
    return jsonify({"employees": employee_data}), 200


@admins.route("/update_employee_xp", methods=["POST"])
@jwt_required()
@routes.user_type(["admin"])
def update_employee_xp():
    data = request.get_json()
    xp = data.get("xp")
    user_id = data.get("user_id")
    try:
        current_user = user.User.from_user_id(user_id=user_id)
    except user.UserDoesntExistError:
        return jsonify({"msg": "Failed: User doesn't exist. "}), 400
    current_user.update_xp(xp)
    return jsonify({"msg": "XP has been updated "}), 201


@admins.route("/all_levels", methods=["GET"])
@jwt_required()
@routes.user_type(["admin"])
def get_all_levels():
    levels = level.Levels.get_all_levels()
    levels_data = [
            {
                "name": l.name,
                "description": l.description
            } for l in levels
        ]
    return jsonify({"levels": levels_data}), 200


@admins.route("/update_employee_levels", methods=["POST"])
@jwt_required()
@routes.user_type(["admin"])
def update_employee_levels():
    data = request.get_json()
    level_id = data.get("level_id")
    user_id = data.get("user_id")
    try:
        current_user = user.User.from_user_id(user_id=user_id)
    except user.UserDoesntExistError as e:
        return jsonify({"msg": f"Failed: User doesn't exist. "}), 400
    current_user.update_level(level_id)
    return jsonify({"msg": "level  has been updated "}), 201
