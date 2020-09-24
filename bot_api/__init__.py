from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from bot_api.config import Config

db = SQLAlchemy()
migrate = Migrate()
rest_api = Api()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from bot_api.api import bp as api_bp

    rest_api.init_app(api_bp)

    app.register_blueprint(api_bp, url_prefix="/api")

    app.logger.setLevel(app.config["LOG_LEVEL"])

    return app


from bot_api import models, urls
