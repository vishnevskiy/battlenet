import unittest
import eventlet
import os
import battlenet

battlenet.Connection.setup(app=os.environ.get('BATTLENET_APP'), eventlet=True)

class EventletTest(unittest.TestCase):
    def setUp(self):
        self.pool = eventlet.GreenPool()

    def test_characters(self):
        names = ['Stanislav', 'Vishnevskiy', 'Spruck', 'Marklevin', 'Tandisse']

        def get_character(name):
            return battlenet.Character(battlenet.UNITED_STATES, 'Nazjatar', name)
        
        for i, character in enumerate(self.pool.imap(get_character, names)):
            self.assertEqual(character.name, names[i])

    def test_realms(self):
        names = ['nazjatar', 'kiljaeden', 'blackrock', 'anubarak']

        def get_realm(name):
            return battlenet.Realm(battlenet.UNITED_STATES, name)

        for i, realm in enumerate(self.pool.imap(get_realm, names)):
            self.assertEqual(realm.slug, battlenet.slugify(names[i]))

if __name__ == '__main__':
    unittest.main()