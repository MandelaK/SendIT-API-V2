import unittest

from run import app
from db_config import db


class ConfigurationTestCase(unittest.TestCase):

    def setUp(self):
        """This method is called before every test and sets up our test"""
        self.client = app.test_client
        self.db = db
