#!/usr/bin/python3
"""
Writing some tests for the console
"""
import unittest
import sqlalchemy
from sqlalchemy.exc import IntegrityError
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
    def setUp(self):
        # Redirect stdout to capture console output
        self.stdout_patch = unittest.mock.patch('sys.stdout',
                                                new_callable=StringIO)
        self.stdout_mock = self.stdout_patch.start()

    def tearDown(self):
        # Clean up and restore stdout
        self.stdout_patch.stop()

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

            cons.onecmd('create Place name="Center" num="00001" \
                        max_guest=10 lat=127.2345 sp="sp_ace" \
                        Pat_mean="Quot\"ed" ignored1 \
                        not_quoted=ignored')
            _id = cons_out.getvalue().strip()

            cons.onecmd(f"show Place {_id}")
            show_out = cons_out.getvalue().strip()
            self.assertIn("'name': 'Center'", show_out)
            self.assertIn("'max_guest': 10", show_out)
            self.assertIn("'lat': 127.2345", show_out)
            self.assertIn("'num': '00001'", show_out)
            self.assertIn("'sp': 'sp ace'", show_out)
            # self.assertIn("'Pat_mean': 'Quot\"ed'", show_out)
            self.assertIn("'Pat_mean': 'Quoted'", show_out)
            self.assertNotIn("'ignored1'", show_out)
            self.assertNotIn("'not_quoted': 'ignored'", show_out)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != "db",
                     "only available in the filestorage")
    def test_db_raise_error_nullable(self):
        """Testing that error is raised when non nullable field is empty"""
        with self.assertRaises(IntegrityError):
            cons = HBNBCommand()
            cons.onecmd('create State')

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != "db",
                     "only available in the filestorage")
    def test_db_create_show(self):
        """Testing create in db"""
        with patch('sys.stdout', new=StringIO()) as cons_out:
            cons = HBNBCommand()
            cons.onecmd('create User email="test@hbnb.tech" password="pass"')
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
            cursor.close()
            db_connect.close()
