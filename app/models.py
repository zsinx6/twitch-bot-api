from datetime import datetime
from app import db


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
