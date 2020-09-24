from flask import jsonify, request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.auth import basic_auth, token_auth
from app.models import Alert, LoginUser, User


class Alerts(Resource):
    method_decorators = [token_auth.login_required]

    def post(self):
        data = request.get_json()
        user = self._create_user(data)
        alert = self._create_alert(data, user)

        json_send = {}
        json_send[alert.id] = {
            "username": user.username,
            "twitch_id": user.twitch_id,
            "profile_image_url": user.profile_image_url,
            "channel_id": alert.channel_id,
            "message_text": alert.message_text,
        }
        return jsonify(json_send)

    def _create_user(self, data):
        username = data.get("username")
        twitch_id = data.get("twitch_id")
        profile_image_url = data.get("profile_image_url")

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

    def _create_alert(self, data, user):
        channel_id = data.get("channel_id")
        message_text = data.get("message_text")

        if not all((channel_id, message_text)):
            abort(400, message="channel_id and message_text should not be empty")

        alert = Alert(channel_id=channel_id, message_text=message_text, user=user)
        db.session.add(alert)
        try:
            db.session.commit()
        except IntegrityError as ex:
            abort(400, message=str(ex))
        return alert


class Tokens(Resource):
    method_decorators = [basic_auth.login_required]

    def get(self):
        token = basic_auth.current_user().get_token()
        db.session.commit()
        return jsonify({"token": token})


class LoginUsers(Resource):
    method_decorators = [token_auth.login_required]

    def post(self):
        data = request.get_json() or {}
        if "username" not in data or "password" not in data:
            abort(400)
        if LoginUser.query.filter_by(username=data["username"]).first():
            return abort(400)
        user = LoginUser()
        user.from_dict(data, new_user=True)
        db.session.add(user)
        db.session.commit()
        response = jsonify(user.to_dict())
        response.status_code = 201
        return response
