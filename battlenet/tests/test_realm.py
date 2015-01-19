# -*- coding: utf-8 -*-

import battlenet
from battlenet import Realm

try:
    import unittest2 as unittest
except ImportError:
    import unittest as unittest
    
class RealmTest(unittest.TestCase):
    def _realm_for(self, region, name, useLocaleEn=False):
        if useLocaleEn:
            realm = self.connection_en.get_realm(region, name)
        else:
            realm = self.connection.get_realm(region, name)
        self.assertEqual(realm.name, name)

    def setUp(self):
        self.connection = battlenet.Connection()
        self.connection_en = battlenet.Connection(locale='en')

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
        self._realm_for(battlenet.KOREA, '가로나')

    def test_realm_korea_en(self):
        self._realm_for(battlenet.KOREA, 'Aegwynn', useLocaleEn=True)

    def test_realm_taiwan(self):
        self._realm_for(battlenet.TAIWAN, '世界之樹')

    def test_realm_taiwan_en(self):
        self._realm_for(battlenet.TAIWAN, 'Aeonus', useLocaleEn=True)

    def test_realm_china(self):
        self._realm_for(battlenet.CHINA, '灰谷')

    def test_realm_china_en(self):
        self._realm_for(battlenet.CHINA, 'Abbendis', useLocaleEn=True)

    def test_unicode(self):
        self._realm_for(battlenet.CHINA, '灰谷')

    def tearDown(self):
        del self.connection
        del self.connection_en

if __name__ == '__main__':
    unittest.main()
