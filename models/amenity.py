#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.place import place_amenity


"""
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', Integer, ForeignKey('places.id')),
    Column('amenity_id', Integer, ForeignKey('amenities.id'))
)
"""


class Amenity(BaseModel):
    """Amenity class"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity,
                                   back_populates="amenity_places")
    id = Column(Integer, primary_key=True)

