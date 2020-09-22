from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api.errors import error_response
from app.models import LoginUser

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = LoginUser.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return LoginUser.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)