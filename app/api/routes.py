from flask import abort, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from app import db, rest_api
from app.api.auth import token_auth
from app.models import User


class new_user(Resource):
    method_decorators = [token_auth.login_required]
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str)
    parser.add_argument("twitch_id", type=int)
    parser.add_argument("profile_image_url", type=str)

    def post(self):
        document = self.parser.parse_args(strict=True)
        username = document.get("username")
        twitch_id = document.get("twitch_id")
        profile_image_url = document.get("profile_image_url")

        user = User(username=username, twitch_id=twitch_id, profile_image_url=profile_image_url)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError as ex:
            abort(400, message=str(ex))

        json_send = {}
        json_send[user.id] = {
            "username": username,
            "twitch_id": twitch_id,
            "profile_image_url": profile_image_url,
        }
        return jsonify(json_send)


rest_api.add_resource(new_user, "/new_user")
