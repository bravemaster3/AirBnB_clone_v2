#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
import os


class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        # if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        # if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
        new = self.value()
        self.assertIsNone(new.name)
