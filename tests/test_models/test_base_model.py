#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            self.name = 'BaseModel'
            self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            try:
                os.remove('file.json')
            except Exception:
                pass

    def test_default(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            i = self.value()
            self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            i = self.value()
            copy = i.to_dict()
            new = BaseModel(**copy)
            self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            i = self.value()
            copy = i.to_dict()
            copy.update({1: 2})
            with self.assertRaises(TypeError):
                new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            i = self.value()
            i.save()
            key = self.name + "." + i.id
            with open('file.json', 'r') as f:
                j = json.load(f)
                self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            i = self.value()
            self.maxDiff = None
            self.assertNotEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                                                              i.__dict__))

    def test_todict(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            i = self.value()
            n = i.to_dict()
            self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            n = {None: None}
            with self.assertRaises(TypeError):
                new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            n = {'Name': 'test'}
            # with self.assertNoRaise(KeyError):
            new = self.value(**n)

    def test_id(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            new = self.value()
            self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            new = self.value()
            self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            prev = self.value()
            self.assertEqual(type(prev.updated_at), datetime.datetime)
            n = prev.to_dict()
            new = BaseModel(**n)
            self.assertTrue(new.created_at == new.updated_at)
            self.assertEqual(prev.created_at, new.created_at)
            self.assertEqual(prev.updated_at, new.updated_at)
