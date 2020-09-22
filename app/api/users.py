from flask import jsonify, request

from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import LoginUser


@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    if "username" not in data or "password" not in data:
        return bad_request("must include username and password fields")
    if LoginUser.query.filter_by(username=data["username"]).first():
        return bad_request("please use a different username")
    user = LoginUser()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    return response
