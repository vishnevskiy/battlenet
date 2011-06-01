import unittest
import os
import battlenet
from battlenet import Realm

battlenet.Connection.setup(app=os.environ.get('BATTLENET_APP'))

class RegionsTest(unittest.TestCase):
    def setUp(self):
        self.connection = battlenet.Connection(os.environ.get('BATTLENET_APP'))

    def test_us(self):
        realms = self.connection.get_all_realms(battlenet.UNITED_STATES)
        self.assertTrue(len(realms) > 0)

    def test_eu(self):
        realms = self.connection.get_all_realms(battlenet.EUROPE)
        self.assertTrue(len(realms) > 0)

    def test_kr(self):
        realms = self.connection.get_all_realms(battlenet.KOREA)
        self.assertTrue(len(realms) > 0)

    def test_tw(self):
        realms = self.connection.get_all_realms(battlenet.TAIWAN)
        self.assertTrue(len(realms) > 0)

    def tearDown(self):
        del self.connection

if __name__ == '__main__':
    unittest.main()

