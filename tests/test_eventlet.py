import os
import battlenet

try:
    import unittest2 as unittest
except ImportError:
    import unittest as unittest

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, eventlet=True)

class EventletTest(unittest.TestCase):
    try:
        import eventlet

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
                self.assertEqual(realm.slug, names[i])
    except ImportError:
        pass

if __name__ == '__main__':
    unittest.main()
