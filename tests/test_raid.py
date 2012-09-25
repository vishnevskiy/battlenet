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

    _characters = (
        (battlenet.UNITED_STATES, 'illidan', 'Zonker'),
        (battlenet.EUROPE, "Lightning's Blade", 'Sejta'),
        (battlenet.KOREA, '굴단', '미스호드진'),
        (battlenet.TAIWAN, '水晶之刺', '憂郁的風'),
        (battlenet.CHINA, '灰谷', '小蠬蝦'),
    )

    def test_ids(self):
        character = Character(self._region, self._realm_name, self._character_name)
        for raid in character.progression['raids']:
            expansion_short, expansion_long = Raid(raid.id).expansion()
            self.assertIsNotNone(expansion_short)
            self.assertIsNotNone(expansion_long)

    def test_order(self):
        expansions = ('wow', 'bc', 'lk', 'cata', 'mop')
        keys = battlenet.EXPANSION.keys()
        keys.sort()
        for i in range(len(keys)):
            self.assertEqual(battlenet.EXPANSION[i][0], expansions[i])

    def test_raids_worldwide(self):
        for region, realm, character_name in self._characters:
            character = Character(region, realm, character_name)
            for raid in character.progression['raids']:
                self.assertIsNotNone(raid)

if __name__ == '__main__':
    unittest.main()
