from collections import OrderedDict
from datetime import datetime, timezone
import uuid

from core import database as db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (Column, Integer, String, ForeignKey, DateTime)
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    files = relationship("File", backref="user", lazy=True)

    def to_dict(self):
        return OrderedDict([
            ("id", self.id),
            ("first_name", self.first_name),
            ("last_name", self.last_name),
            ("email", self.email)
        ])

class File(db.Model):
    id = Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    url = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # Using timezone-aware datetime
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # ForeignKey to link to User

    def __init__(self, filename, url, user_id):
        self.filename = filename
        self.url = url
        self.user_id = user_id

