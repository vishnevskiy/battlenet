# -*- coding: utf-8 -*-

import unittest
import os
import battlenet
import datetime
from battlenet import Character
from battlenet import Raid

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)


class RaidTest(unittest.TestCase):

    _character_name = 'Sejta'
    _region = battlenet.EUROPE
    _realm_name = "Lightning's Blade"

    def test_ids(self):
        character = Character(self._region, self._realm_name, self._character_name)
        for raid in character.progression['raids']:
            expansion_short, expansion_long = Raid(raid.id).expansion()
            self.assertIsNotNone(expansion_short)
            self.assertIsNotNone(expansion_long)

    def test_order(self):
        expansions = ('wow', 'bc', 'lk', 'cata')
        keys = battlenet.EXPANSION.keys()
        keys.sort()
        for i in range(len(keys)):
            self.assertEqual(battlenet.EXPANSION[i][0], expansions[i])

if __name__ == '__main__':
    unittest.main()
