#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker
from models.review import Review
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from models.amenity import Amenity



Base = declarative_base()
"""
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
"""

class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    city_id = Column(String(60), nullable=False)
    user_id = Column(String(60), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship("Review", backref="place",
                           cascade="all, delete-orphan")
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                                 Column('amenity_id', String(60),
                                        ForeignKey('amenities.id'),
                                        primary_key=True, nullable=False)
                                        )
    
    amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False, backref="places")
    
    @property
    def reviews(self):
        """
        for FileStorage: getter attribute reviews that returns
        the list of Review instances with place_id equals to the current
        Place.id => It will be the FileStorage relationship
        between Place and Review
        """
        from models import storage
        d_review = storage.all(Review)
        matching_reviews = [
            review for review in d_review.values() if review.place_id == self.id
        ]
        return matching_reviews
    

    @property
    def amenities(self):
        """
        Getter attribute amenities that returns the list of Amenity
        instances based on
        the attribute amenity_ids that contains all
        Amenity.id linked to the Place
        """
        if self.amenity_ids:
            return [session.query(Amenity).get(int(amenity_id)) for
                    amenity_id in self.amenity_ids.split(",")]
        else:
            return []
        
    @amenities.setter
    def amenities(self, amenity):
        if isinstance(amenity, Amenity):
            if self.amenity_ids:
                self.amenity_ids += f",{amenity.id}"
            else:
                self.amenity_ids = str(amenity.id)
