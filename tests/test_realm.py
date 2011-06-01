import unittest
import os
from battlenet.connection import Connection
from battlenet.things import Realm

Connection.setup(app=os.environ.get('BATTLENET_APP'))

class RealmTest(unittest.TestCase):
    def setUp(self):
        self.connection = Connection(os.environ.get('BATTLENET_APP'))

    def test_realm_by_name(self):
        name = "Kil'jaeden"

        realm = self.connection.get_realm(Connection.US, name)
        self.assertEqual(name, realm.name)

        realm = Realm(Connection.US, name)
        self.assertEqual(name, realm.name)

    def test_realm_by_slug(self):
        slug = 'kiljaeden'

        realm = self.connection.get_realm(Connection.US, slug)

        self.assertEqual(slug, realm.slug)

    def test_all_realms(self):
        realms = self.connection.get_all_realms(Connection.US)

        self.assertGreater(len(realms), 0)

    def test_realm_type(self):
        realm = self.connection.get_realm(Connection.US, 'nazjatar')

        self.assertEqual(realm.type, Realm.PVP)

    def test_realm_population(self):
        realm = self.connection.get_realm(Connection.US, 'nazjatar')

        self.assertEqual(realm.population, Realm.LOW)

    def tearDown(self):
        del self.connection

if __name__ == '__main__':
    unittest.main()