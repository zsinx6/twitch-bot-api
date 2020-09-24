import base64
import os
from datetime import datetime, timedelta

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from bot_api import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    twitch_id = db.Column(db.Integer, nullable=False, unique=True)
    profile_image_url = db.Column(db.Text)
    alerts = db.relationship("Alert", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer)
    message_text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    streams = db.relationship("OnlineAlert", backref="alert", lazy=True)

    __table_args__ = (db.UniqueConstraint("channel_id", "user_id", name="_user_channel_uc"),)

    def __repr__(self):
        return f"Alert {self.channel_id} - {self.user_id}"


class OnlineAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stream_title = db.Column(db.Text)
    thumbnail_url = db.Column(db.Text)
    started_at = db.Column(db.DateTime)
    message_id = db.Column(db.Integer)
    message_edited = db.Column(db.Boolean, nullable=False, default=False)
    is_online = db.Column(db.Boolean, nullable=False, default=False)
    vod_url = db.Column(db.Text, default="", unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    alert_id = db.Column(db.Integer, db.ForeignKey("alert.id"))

    def __repr__(self):
        return f"OnlineAlert {self.message_id}"


class LoginUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    @staticmethod
    def check_token(token):
        user = LoginUser.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self):
        data = {"id": self.id, "username": self.username}
        return data

    def from_dict(self, data, new_user=False):
        for field in ["username"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])
