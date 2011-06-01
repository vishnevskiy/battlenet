import unittest
import os
import battlenet

class EventletTest(unittest.TestCase):
    def setUp(self):
        self.connection = battlenet.Connection(os.environ.get('BATTLENET_APP'))

    def test_character_not_found(self):
        self.assertRaises(battlenet.APIError,
            lambda: self.connection.get_character(battlenet.UNITED_STATES, 'Fake Realm', 'Fake Character'))

    def test_realm_not_found(self):
        self.assertRaises(battlenet.RealmNotFound, lambda: self.connection.get_realm(battlenet.EUROPE, 'Fake Realm'))

    def tearDown(self):
        del self.connection

if __name__ == '__main__':
    unittest.main()