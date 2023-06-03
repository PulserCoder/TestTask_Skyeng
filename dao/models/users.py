from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from setup_db import Base


class User(Base):
    """USER table"""
    __tablename__ = 'users'
    userid = Column(Integer(), primary_key=True)
    username = Column(String(150))
    first_name = Column(String(150))
    last_name = Column(String(150))
    date_registration = Column(DateTime, default=datetime.utcnow)

class UserSchema(Schema):
    """Schema of the USER table"""
    id = fields.Int()
    userid = fields.Int()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    date_registration = fields.DateTime()
