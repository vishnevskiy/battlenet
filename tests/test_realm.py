# -*- coding: utf-8 -*-

import battlenet
from battlenet import Realm

try:
    import unittest2 as unittest
except ImportError:
    import unittest as unittest
    
class RealmTest(unittest.TestCase):
    def setUp(self):
        self.connection = battlenet.Connection()

    def test_realm_by_name(self):
        name = "Kiljaeden"

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

    def test_realms(self):
        names = sorted(['Blackrock', 'Nazjatar'])

        realms = self.connection.get_realms(battlenet.UNITED_STATES, names)

        self.assertEqual(names, sorted([realm.name for realm in realms]))

    def test_realm_type(self):
        realm = self.connection.get_realm(battlenet.UNITED_STATES, 'nazjatar')

        self.assertEqual(realm.type, Realm.PVP)

    def test_realm_population(self):
        realm = self.connection.get_realm(battlenet.UNITED_STATES, 'nazjatar')

        self.assertIn(realm.population, [Realm.LOW, Realm.MEDIUM, Realm.HIGH])

    def test_unicode(self):
        realm = self.connection.get_realm(battlenet.EUROPE, 'Термоштепсель')

        self.assertEqual(realm.name, 'Thermaplugg')

    def tearDown(self):
        del self.connection

if __name__ == '__main__':
    unittest.main()
