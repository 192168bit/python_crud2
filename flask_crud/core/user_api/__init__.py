from flask import Blueprint

user_api_blueprint = Blueprint("user_api_blueprint", __name__)
file_upload_api_blueprint = Blueprint("file_upload_api_blueprint", __name__)

from . import (
    file_upload_routes,
    user_routes # noqa F401, # noqa F401
)