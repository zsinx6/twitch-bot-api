from flask import Blueprint

bp = Blueprint("api", __name__)

from bot_api.api import resources
