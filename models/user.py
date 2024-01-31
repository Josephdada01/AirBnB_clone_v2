#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import models
from os import getenv


class User(BaseModel, Base):
    """This class defines a user by various attributes s"""

    if getenv('HBNB_TYPE_STORAGE') == 'db':

        __table__ = 'users'
        email = Column(String(128), nullable=False)

        password = Column(String(128), nullable=False)

        first_name = Column(String(128), nullable=True)

        last_name = Column(String(128), nullable=True)

        places = relationship(
                "Place",
                backref="user",
                cascade="delete")

        reviews = relationship(
                "Review",
                backref="user",
                )
    else:
        email = ""
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """initialize users"""
        super().init__(*args, **kwargs)