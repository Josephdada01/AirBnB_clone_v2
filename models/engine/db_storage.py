#!/usr/bin/python3
"""DBStorage module"""
import os
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DBStorage:
    """This class represents the implementation for the DBStorage"""

    __engine = None
    __session = None

    def __init__(self):
        '''The constructor of the DBStorage'''
        user = os.environ.get('HBNB_MYSQL_USER')
        passwd = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        db = os.environ.get('HBNB_MYSQL_DB')
        env = os.environ.get('HBNB_ENV')

        if self.__engine is None:
            url = (
                    "mysql+mysqldb://{}:{}@{}/{}".format(
                        user, passwd, host, db
                        )
                    )
            self.__engine = create_engine(url, pool_pre_ping=True)

            if (env == 'test'):
                Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''query on the current database session'''
        db_storage = {}
        if (cls):
            query = self.__session.query(cls).all()

            for item in query:
                key = "{}.{}".format(type(item).__name__, item.id)
                db_storage[key] = item
        else:
            object_types = [User, State, City, Amenity, Place, Review]

            for obj in object_types:
                query = self.__session.query(obj).all()
                for item in query:
                    key = "{}.{}".format(type(item).__name__, item.id)
                    db_storage[key] = item

        return db_storage

    def new(self, obj):
        '''add the object to the current database session'''
        if (obj):
            self.__session.add(obj)

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''
        Delete from the current database session obj if not None
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''create all tables in the databas'''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                self.__engine, expire_on_commit=False
                )
        self.__session = scoped_session(session_factory)

    def close(self):
        """ Close the session"""
        self.__session.close()