# -*- coding: utf-8 -*-

import battlenet
from battlenet import Realm

try:
    import unittest2 as unittest
except ImportError:
    import unittest as unittest
    
class RealmTest(unittest.TestCase):
    def _realm_for(self, region, name):
        realm = self.connection.get_realm(region, name)
        self.assertEqual(realm.name, name)

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

    def test_all_realms_europe(self):
        realms = self.connection.get_all_realms(battlenet.EUROPE)

        self.assertGreater(len(realms), 0)

    def test_all_realms_korea(self):
        realms = self.connection.get_all_realms(battlenet.KOREA)

        self.assertGreater(len(realms), 0)

    def test_all_realms_taiwan(self):
        realms = self.connection.get_all_realms(battlenet.TAIWAN)

        self.assertGreater(len(realms), 0)

    def test_all_realms_china(self):
        realms = self.connection.get_all_realms(battlenet.CHINA)

        self.assertGreater(len(realms), 0)

    def test_realms(self):
        names = sorted(['Blackrock', 'Nazjatar'])

        realms = self.connection.get_realms(battlenet.UNITED_STATES, names)

        self.assertEqual(names, sorted([realm.name for realm in realms]))

    def test_realm_type(self):
        realm = self.connection.get_realm(battlenet.UNITED_STATES, 'Nazjatar')

        self.assertEqual(realm.type, Realm.PVP)

    def test_realm_population(self):
        realm = self.connection.get_realm(battlenet.UNITED_STATES, 'Nazjatar')

        self.assertIn(realm.population, [Realm.LOW, Realm.MEDIUM, Realm.HIGH])

    def test_realm_united_state(self):
        self._realm_for(battlenet.UNITED_STATES, 'Blackrock')

    def test_realm_europe(self):
        self._realm_for(battlenet.EUROPE, 'Khaz Modan')

    def test_realm_korea(self):
        self._realm_for(battlenet.KOREA, 'Aegwynn')

    def test_realm_taiwan(self):
        self._realm_for(battlenet.TAIWAN, 'Aeonus')

    def test_realm_china(self):
        self._realm_for(battlenet.CHINA, '灰谷')

    def test_unicode(self):
        self._realm_for(battlenet.CHINA, '灰谷')

    def tearDown(self):
        del self.connection

if __name__ == '__main__':
    unittest.main()
