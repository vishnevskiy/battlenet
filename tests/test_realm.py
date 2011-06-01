import unittest
import os
import battlenet
from battlenet import Realm

battlenet.Connection.setup(app=os.environ.get('BATTLENET_APP'))

class RealmTest(unittest.TestCase):
    def setUp(self):
        self.connection = battlenet.Connection(os.environ.get('BATTLENET_APP'))

    def test_realm_by_name(self):
        name = "Kil'jaeden"

        realm = self.connection.get_realm(battlenet.UNITED_STATES, name)
        self.assertEqual(name, realm.name)

        realm = Realm(battlenet.UNITED_STATES, name)
        self.assertEqual(name, realm.name)

    def test_realm_by_slug(self):
        slug = 'kiljaeden'

        realm = self.connection.get_realm(battlenet.UNITED_STATES, slug)

        self.assertEqual(slug, realm.slug)

    def test_all_realms(self):
        realms = self.connection.get_all_realms(battlenet.UNITED_STATES)

        self.assertGreater(len(realms), 0)

    def test_realm_type(self):
        realm = self.connection.get_realm(battlenet.UNITED_STATES, 'nazjatar')

        self.assertEqual(realm.type, Realm.PVP)

    def test_realm_population(self):
        realm = self.connection.get_realm(battlenet.UNITED_STATES, 'nazjatar')

        self.assertEqual(realm.population, Realm.LOW)

    def tearDown(self):
        del self.connection

if __name__ == '__main__':
    unittest.main()