from flask import jsonify, request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.auth import token_auth
from app.models import Alert, User


class Alerts(Resource):
    method_decorators = [token_auth.login_required]

    def post(self):
        document = request.get_json()
        user = self._create_user(document)
        alert = self._create_alert(document, user)

        json_send = {}
        json_send[alert.id] = {
            "username": user.username,
            "twitch_id": user.twitch_id,
            "profile_image_url": user.profile_image_url,
            "channel_id": alert.channel_id,
            "message_text": alert.message_text,
        }
        return jsonify(json_send)

    def _create_user(self, document):
        username = document.get("username")
        twitch_id = document.get("twitch_id")
        profile_image_url = document.get("profile_image_url")

        if not all((username, twitch_id, profile_image_url)):
            abort(400, message="username, twitch_id and profile_image_url should not be empty")

        user = User.query.filter_by(username=username, twitch_id=twitch_id).first()
        if user:
            return user

        user = User(username=username, twitch_id=twitch_id, profile_image_url=profile_image_url)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError as ex:
            abort(400, message=str(ex))
        return user

    def _create_alert(self, document, user):
        channel_id = document.get("channel_id")
        message_text = document.get("message_text")

        if not all((channel_id, message_text)):
            abort(400, message="channel_id and message_text should not be empty")

        alert = Alert(channel_id=channel_id, message_text=message_text, user=user)
        db.session.add(alert)
        try:
            db.session.commit()
        except IntegrityError as ex:
            abort(400, message=str(ex))
        return alert
