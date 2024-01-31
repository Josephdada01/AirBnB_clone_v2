#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Amenity(BaseModel, Base):
    """Amenity class"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':

        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("place",
                                   secondary='place_amenity',
                                   viewonly=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """intializing amenity"""
        super().__init__(*args, **kwargs)
