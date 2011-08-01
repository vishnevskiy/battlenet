import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest as unittest
try:
    ## If we can import eventlet go ahead and set up the connection to use eventlet.
    ## Otherwise, don't set up the connection as we're not going to do this test.
    import eventlet
    battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, eventlet=True)
except:
    pass
import os
import battlenet

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')



class EventletTest(unittest.TestCase):
    try:
        ## If we could load eventlet then go ahead and run the tests, otherwise just skip them.
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
    except:
        pass

if __name__ == '__main__':
    unittest.main()
