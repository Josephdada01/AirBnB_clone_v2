#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    """ The city class, contains state ID and name """

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'cities'

        id = Column(String(60), primary_key=True, nullable=False)

        state_id = Column(
                String(60),
                ForeignKey('states.id'), nullable=False
                )

        name = Column(String(128), nullable=False)

        places = relationship("Place",
                              backref="cities",
                              cascade="all, delete"
                              )
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """initialize city"""
        super().__init__(*args, **kwargs)
