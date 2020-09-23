from app import rest_api
from app.api.routes import Alerts

rest_api.add_resource(Alerts, "/alerts")
