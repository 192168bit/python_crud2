from collections import OrderedDict
import uuid

from core import database as db

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, text, Text, DateTime, DECIMAL, Float)
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    def to_dict(self):
        return OrderedDict([
            ("id", self.id),
            ("first_name", self.first_name),
            ("last_name", self.last_name),
            ("email", self.email)
        ])