#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
# from models.base_model import BaseModel
from models.state import State
from models.user import User
from models import storage
import MySQLdb
import os
import time


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        if (os.getenv('HBNB_TYPE_STORAGE') != "db"):
            self.n_states = 0
            self.n_users = 0
            del_list = []
            # for key in storage._FileStorage__objects.keys():
            for key in storage.all().keys():
                del_list.append(key)
            for key in del_list:
                # del storage._FileStorage__objects[key]
                del storage.all()[key]

        if (os.getenv('HBNB_TYPE_STORAGE') == "db"):
            self.n_states = len(storage.all(State))
            self.n_users = len(storage.all(User))
            # db_connect = MySQLdb.connect(
            #     user=os.getenv('HBNB_MYSQL_USER'),
            #     passwd=os.getenv('HBNB_MYSQL_PWD'),
            #     db=os.getenv('HBNB_MYSQL_DB'),
            #     host=os.getenv('HBNB_MYSQL_HOST'),
            #     port=3306,
            #     autocommit=True
            # )

            # cursor = db_connect.cursor()
            # cursor.execute("SELECT * FROM states;")
            # rows = cursor.fetchall()
            # self.n_states = len(rows)

            # cursor.execute("SELECT * FROM users;")
            # rows = cursor.fetchall()
            # self.n_users = len(rows)
            # cursor.close()
            # db_connect.close()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except Exception:
            pass

    # @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
    #                  "only available in the filestorage")
    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertGreaterEqual(len(storage.all()),
                                self.n_states + self.n_users)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = State(name="California")
        for obj in storage.all().values():
            temp = obj
            self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = State(name="California")
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    # @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
    #                  "only available in the filestorage")
    def test_all_filtering(self):
        """ returned __objects only contains the specified class """
        new_base = User(email="test@hbnb.tech", password="pass")
        new_base.save()
        new_state = State(name="California")
        new_state.save()
        temp1 = {}
        temp1.update(storage.all(State))
        temp1.update(storage.all(User))
        self.assertEqual(len(temp1), 2 + self.n_states + self.n_users)
        temp2 = storage.all(State)
        self.assertEqual(len(temp2), 1 + self.n_states)

        # for obj in temp2.values():
        #     self.assertEqual(obj.__dict__['id'], new_state.__dict__['id'])
        self.assertIn(f"State.{new_state.id}", temp2.keys())

    # @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
    #                  "only available in the filestorage")
    def test_base_model_instantiation(self):
        """ File is not created on State save """
        if os.getenv('HBNB_TYPE_STORAGE') != "db":
            new = State(name="California")
            self.assertFalse(os.path.exists('file.json'))

    # @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
    #                  "only available in the filestorage")
    def test_empty(self):
        """ Data is saved to file """
        if os.getenv('HBNB_TYPE_STORAGE') != "db":
            new = State(name="California")
            # thing = new.to_dict()
            new.save()
            # new2 = State(**thing)
            self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = State(name="California")
        storage.save()
        if os.getenv('HBNB_TYPE_STORAGE') != "db":
            self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = State(name="California")
        new.save()
        storage.reload()
        # for obj in storage.all().values():
        #     loaded = obj
        #     self.assertEqual(new.__dict__['id'], loaded.__dict__['id'])
        self.assertIn(f'State.{new.id}', storage.all().keys())

    # @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
    #                  "only available in the filestorage")
    def test_reload_empty(self):
        """ Load from an empty file """
        if os.getenv('HBNB_TYPE_STORAGE') != "db":
            with open('file.json', 'w') as f:
                pass
            with self.assertRaises(ValueError):
                storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    # @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
    #                  "only available in the filestorage")
    def test_base_model_save(self):
        """ State save method calls storage save """
        new = State(name="California")
        new.save()
        if os.getenv('HBNB_TYPE_STORAGE') != "db":
            self.assertTrue(os.path.exists('file.json'))

    # @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
    #                  "only available in the filestorage")
    def test_type_path(self):
        """ Confirm __file_path is string """
        if os.getenv('HBNB_TYPE_STORAGE') != "db":
            self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = State(name="California")
        new.save()
        _id = new.__dict__['id']
        # for key in storage.all().keys():
        #     temp = key
        #     self.assertEqual(temp, 'State' + '.' + _id)
        self.assertIn('State' + '.' + _id, storage.all().keys())

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        if os.getenv('HBNB_TYPE_STORAGE') != "db":
            from models.engine.file_storage import FileStorage
            self.assertEqual(type(storage), FileStorage)
        else:
            from models.engine.db_storage import DBStorage
            self.assertEqual(type(storage), DBStorage)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
                     "only available in the filestorage")
    def test_delete_exists(self):
        """ Testing the delete method """
        new = State(name="California")
        new.save()
        self.assertTrue(os.path.exists('file.json'))
        for obj in storage.all().values():
            loaded = obj
            self.assertEqual(new.__dict__['id'], loaded.__dict__['id'])
        storage.delete(new)
        for obj in storage.all().values():
            self.assertIsNone(obj.__dict__['id'])

    def test_delete_notexist(self):
        """ Testing the delete method """
        new = State(name="California")
        new.save()
        storage.delete(new)
        storage.delete(new)  # Do nothing when it doesn't exist


if __name__ == "__main__":
    if (os.getenv('HBNB_TYPE_STORAGE') == "db"):
        storage.reload()
    test_fileStorage()
