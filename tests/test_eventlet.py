import unittest
import eventlet
import os
from battlenet.connection import Connection
from battlenet.things import Character, Realm
from battlenet.utils import slugify

Connection.setup(app=os.environ.get('BATTLENET_APP'), eventlet=True)

class EventletTest(unittest.TestCase):
    def setUp(self):
        self.pool = eventlet.GreenPool()

    def test_characters(self):
        names = ['Stanislav', 'Vishnevskiy', 'Spruck', 'Marklevin', 'Tandisse']

        for i, character in enumerate(self.pool.imap(lambda name: Character(Connection.US, 'Nazjatar', name), names)):
            self.assertEqual(character.name, names[i])

    def test_realms(self):
        names = ['nazjatar', 'kiljaeden', 'blackrock', 'anubarak']

        for i, realm in enumerate(self.pool.imap(lambda name: Realm(Connection.US, name), names)):
            self.assertEqual(realm.slug, slugify(names[i]))

if __name__ == '__main__':
    unittest.main()