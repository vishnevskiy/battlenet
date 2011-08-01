import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest as unittest
import os
import battlenet

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')


class RegionsTest(unittest.TestCase):
    def setUp(self):
        self.connection = battlenet.Connection(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

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
