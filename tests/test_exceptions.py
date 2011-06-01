import unittest
import os
from battlenet.connection import Connection
from battlenet.exceptions import APIError, RealmNotFound

class EventletTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection(os.environ.get('BATTLENET_APP'))

    def test_character_not_found(self):
        self.assertRaises(APIError, lambda: self.connection.get_character(Connection.US, 'Fake Realm', 'Fake Character'))

    def test_realm_not_found(self):
        self.assertRaises(RealmNotFound, lambda: self.connection.get_realm(Connection.US, 'Fake Realm'))

    def tearDown(self):
        del self.connection

if __name__ == '__main__':
    unittest.main()