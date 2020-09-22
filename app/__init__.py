import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config


flask_app = Flask(__name__)
flask_app.config.from_object(Config)

_formatter = "%(levelname)-8s : %(module)-10s : %(funcName)-25s :%(lineno)-3d : %(message)s"
_logger = logging.getLogger(__name__)
logging.basicConfig(level=flask_app.config["LOG_LEVEL"], format=_formatter)

db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

from app import routes, models
