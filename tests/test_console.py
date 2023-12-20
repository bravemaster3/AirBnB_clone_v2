#!/usr/bin/python3
"""
Writing some tests for the console
"""
import unittest
import sqlalchemy
import json
import os
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
import MySQLdb


class TestConsole(unittest.TestCase):
    """
    Test class for the console.
    """
    def get_console(self, command):
        """Method for getting the console"""
        with patch('sys.stdout', new=StringIO()) as cons_out:
            cons = HBNBCommand()
            cons.onecmd(command)
            return cons_out.getvalue().strip()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
                     "only available in the filestorage")
    def test_fs_create(self):
        """Testing the new create features"""
        output = self.get_console('create City name="Texas"')
        self.assertIn(f'City.{output}', storage.all().keys())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == "db",
                     "only available in the filestorage")
    def test_fs_create_show(self):
        """Testing create and show to check that int, float are casted"""
        with patch('sys.stdout', new=StringIO()) as cons_out:
            cons = HBNBCommand()

            cons.onecmd('create Place name="Center" num="00001" max_guest=10 lat=127.2345 sp="sp_ace"')
            _id = cons_out.getvalue().strip()

            cons.onecmd(f"show Place {_id}")
            show_out = cons_out.getvalue().strip()
            self.assertIn("'name': 'Center'", show_out)
            self.assertIn("'max_guest': 10", show_out)
            self.assertIn("'lat': 127.2345", show_out)
            self.assertIn("'num': '00001'", show_out)
            self.assertIn("'sp': 'sp ace'", show_out)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != "db",
                     "only available in the filestorage")
    def test_db_create_show(self):
        """Testing create in db"""
        with patch('sys.stdout', new=StringIO()) as cons_out:
            cons = HBNBCommand()

            #Test that an error is raised when no arguments are passed
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons.onecmd('create City')

            cons.onecmd('create User email="test@hbnb.tech" password="my_pass"')
            _id = cons_out.getvalue().strip()

            db_connect = MySQLdb.connect(
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB'),
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306
            )
            cursor = db_connect.cursor()
            cursor.execute(f'SELECT * FROM users WHERE id="{_id}"')
            row = cursor.fetchone()
            self.assertTrue(row is not None)
