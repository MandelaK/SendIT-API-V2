import unittest

from app import create_app
from db_config import destroy_tables


class BaseTestClass(unittest.TestCase):
    """This is our base test class"""

    def setUp(self):
        """This will be run before each test"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app.testing = True

    def tearDown(self):
        destroy_tables()
