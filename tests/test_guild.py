# -*- coding: utf-8 -*-

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest as unittest
import os
import battlenet
import datetime
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

        character = guild.get_leader()

        self.assertEqual(character.name, 'Clí')

    def test_lazyload_member_character(self):
        guild = Guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence')

        character = guild.get_leader()

        self.assertRegexpMatches(character.get_full_class_name(), r'^(Holy|Protection|Retribution) Paladin$')

    def test_achievements(self):
        guild = Guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence', fields=[Guild.ACHIEVEMENTS])

        for id_, completed_ts in guild.achievements.items():
            self.assertIsInstance(id_, int)
            self.assertIsInstance(completed_ts, datetime.datetime)

    def test_perks(self):
        guild = Guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence')

        self.assertGreater(len(guild.perks), 1)

    def test_rewards(self):
        guild = Guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence')

        self.assertGreater(len(guild.rewards), 1)

if __name__ == '__main__':
    unittest.main()
