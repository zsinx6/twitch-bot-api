from bot_api import rest_api
from bot_api.api.resources import Alerts, LoginUsers, Tokens

rest_api.add_resource(Alerts, "/alerts")
rest_api.add_resource(Tokens, "/tokens")
rest_api.add_resource(LoginUsers, "/users")
