from app import rest_api
from app.api.resources import Alerts

rest_api.add_resource(Alerts, "/alerts")
