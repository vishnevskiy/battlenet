# -*- coding: utf-8 -*-

import unittest
import os
import battlenet
from battlenet import Guild

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

class GuildTest(unittest.TestCase):
    def test_general(self):
        guild = Guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence')

        self.assertEqual(guild.name, 'Excellence')
        self.assertEqual(str(guild), 'Excellence')

        self.assertEqual(guild.get_realm_name(), 'Nazjatar')
        self.assertEqual(guild.realm.name, 'Nazjatar')
        self.assertEqual(str(guild.realm), 'Nazjatar')

    def test_len(self):
        guild = Guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence', fields=[Guild.MEMBERS])
        
        self.assertGreater(len(guild), 1)

    def test_leader(self):
        guild = Guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence', fields=[Guild.MEMBERS])

        character =  guild.get_leader()

        self.assertEqual(character.name, 'Clí')

if __name__ == '__main__':
    unittest.main()
