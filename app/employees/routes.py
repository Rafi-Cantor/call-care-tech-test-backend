from flask_jwt_extended import jwt_required, get_current_user
from flask import jsonify, request
from app.employees import employees
from objects import user, level
from app.auth import routes


@employees.route("/<user_id>", methods=["GET"])
@jwt_required()
@routes.user_type(["employee"])
def get_employee_by_id(user_id):
    try:
        employee = user.User.from_user_id(user_id)
    except user.UserDoesntExistError:
        return jsonify({"msg": "Employee not found"}), 404

    employee_data = {
        "user_id": employee.user_id,
        "user_name": employee.user_name,
        "level_id": employee.current_level_id,
        "xp": employee.xp,
    }
    return jsonify({"employee": employee_data}), 200


@employees.route("/all_levels", methods=["GET"])
@jwt_required()
@routes.user_type(["employee"])
def get_all_levels():
    levels = level.Levels.get_all_levels()
    levels_data = [
            {
                "name": l.name,
                "description": l.description,
                "code": l.code
            } for l in levels
        ]
    return jsonify({"levels": levels_data}), 200




