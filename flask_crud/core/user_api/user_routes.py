from . import user_api_blueprint
from core.schema import UserSchema, GetUserSchema
from apifairy import body
from core.models import User
from core import database
from flask import request, jsonify
from collections import OrderedDict
import json

get_user_schema = GetUserSchema(many=True)
user_schema = UserSchema()


@user_api_blueprint.route("/users", methods=["GET"])
def all_users():
    users = User.query.order_by(User.id.asc()).all()
    users_data = [user.to_dict() for user in users]
    response_data = json.dumps({"users": users_data})

    return (response_data), 200

@user_api_blueprint.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user:
        response_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        return jsonify(response_data), 200
    else:
        return jsonify({"error": "User not found"}), 404


@user_api_blueprint.route("/users", methods=["POST"])
@body(user_schema)
def add_user(kwargs):
    new_user = User(**kwargs)
    database.session.add(new_user)
    database.session.commit()
    response_data = OrderedDict(
        [
            ("message", "User added successfully"),
            (
                "user",
                OrderedDict(
                    [
                        ("id", new_user.id),
                        ("first_name", new_user.first_name),
                        ("last_name", new_user.last_name),
                        ("email", new_user.email),
                    ]
                ),
            ),
        ]
    )
    return jsonify(response_data), 201


@user_api_blueprint.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)
    database.session.commit()
    response_data = OrderedDict(
        [
            ("message", "User added successfully"),
            (
                "user",
                OrderedDict(
                    [
                        ("id", user.id),
                        ("first_name", user.first_name),
                        ("last_name", user.last_name),
                        ("email", user.email),
                    ]
                ),
            ),
        ]
    )
    return jsonify(response_data), 200


@user_api_blueprint.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    database.session.delete(user)
    database.session.commit()
    return jsonify({"message": "User deleted successfully"})
