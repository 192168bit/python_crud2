from flask import Blueprint

user_api_blueprint = Blueprint("user_api_blueprint", __name__)

from . import (
    user_routes, # noqa F401
)