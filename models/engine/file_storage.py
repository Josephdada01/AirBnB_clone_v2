#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
import uuid


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage,
        that returns the list of objects of one type of class

        Args:
            cls: class to be filter out and displayed
        """

        if cls is None:
            return FileStorage.__objects

        if (cls not in FileStorage.__objects):
            return FileStorage.__objects
        else:
            for key in FileStorage.__objects.keys():
                if (key == cls):
                    return (FileStorage.__objects[key])

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if hasattr(obj, 'id'):
            self.all().update({
                "{}.{}".format(obj.__class__.__name__, obj.id): obj
                })
        else:
            obj.id = str(uuid.uuid4())
            self.all().update({
                "{}.{}".format(obj.__class__.__name__, obj.id): obj
                })

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside

        Args:
            obj: the class name
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """a public method def close(self):: call reload()
        method for deserializing the JSON file to objects"""
        self.reload()
