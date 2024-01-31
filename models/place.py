#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.review import Review
from os import getenv
import models

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column(
                'place_id', String(60), ForeignKey('places.id'),
                primary_key=True, nullable=False
                ),
            Column(
                'amenity_id', String(60), ForeignKey('amenities.id'),
                primary_key=True, nullable=False
                )
        )

class Place(BaseModel, Base):
    """ A place to stay """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'places'
        city_id = Column(
            String(60),
            ForeignKey('cities.id'),
            nullable=False
            )

        user_id = Column(
                String(60),
                ForeignKey('users.id'),
                nullable=False
                )

        name = Column(
                String(128),
                nullable=False
                )

        description = Column(
                String(1024),
                nullable=True
                )

        number_rooms = Column(
                Integer,
                nullable=False,
                default=0
                )

        number_bathrooms = Column(
                Integer,
                nullable=False,
                default=0
                )

        max_guest = Column(
                Integer,
                nullable=False,
                default=0
                )

        price_by_night = Column(
                Integer,
                nullable=False,
                default=0
                )

        latitude = Column(
                Float,
                nullable=True
                )

        longitude = Column(
                Float,
                nullable=True
                )

        reviews = relationship(
                "Review",
                backref="place",
                cascade="all, delete"
                )
        amenities = relationship("Amenity",
                                 secondary='place_amenity',
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes place"""
        super().__init__(*args, **kwargs)
        
            
    @property
    def reviews(self):
        """
        for FileStorage: getter attribute reviews that returns
        the list of Review instances with place_id equals to the current
        Place.id => It will be the FileStorage relationship
        between Place and Review
        """

        matching_reviews = []

        matching_obj = models.storage.all(Review)

        for key, value in matching_obj.items():
            if value.place_id == self.id:
                matching_reviews.append(value)

        return matching_reviews
    """
    @property
    def amenities(self):

        returns the list of Amenity instances based on the attribute
        amenity_ids that contains all Amenity.id linked to the Place

        amenities_list = []

        amenities_obj = models.storage.all(Amenity)

        for amenity in amenities_obj.values():
            if self.id in amenity.amenity_ids:
                amenities_list.append(amenity)

        return amenities_list
    """

    @property
    def amenities(self):
        """
        Returns the list of Amenity instances linked to the Place.
        """
        return self.amenities
    
    @amenities.setter
    def amenities(self, amenity):
        """
        Handles append method for adding an Amenity
        to the amenities relationship.
        """
        if isinstance(amenity, Amenity):
            if amenity not in self.amenities:
                self.amenities.append(amenity)


