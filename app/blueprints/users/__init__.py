from flask import Blueprint

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")

from . import routes