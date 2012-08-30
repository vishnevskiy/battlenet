# -*- coding: utf-8 -*-

import os
import battlenet
import datetime
from battlenet import Character

try:
    import unittest2 as unittest
except ImportError:
    import unittest as unittest

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)


class CharacterTest(unittest.TestCase):
    def test_general(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Stanislav')

        self.assertEqual(character.name, 'Stanislav')
        self.assertEqual(str(character), 'Stanislav')

        self.assertEqual(character.get_realm_name(), 'Nazjatar')
        self.assertEqual(character.realm.name, 'Nazjatar')
        self.assertEqual(str(character.realm), 'Nazjatar')

        self.assertEqual(character.faction, Character.HORDE)

        self.assertEqual(character.get_race_name(), Character.BLOOD_ELF)

        self.assertEqual(character.get_class_name(), Character.DEATH_KNIGHT)

        self.assertIsInstance(character.level, int)
        self.assertGreaterEqual(character.level, 85)

        self.assertIsInstance(character.achievement_points, int)

        self.assertEqual(character.gender, Character.MALE)

    def test_guild(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Stanislav', fields=[Character.GUILD])

        self.assertEqual(character.guild.name, 'Excellence')

    def test_stats(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Stanislav', fields=[Character.STATS])

        self.assertIsInstance(character.stats.agility, int)

    def test_professions(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Stanislav', fields=[Character.PROFESSIONS])

        primary = character.professions['primary']

        tailoring = primary[0]
        enchanting = primary[1]

        self.assertEqual(tailoring.name, Character.MINING)
        self.assertIsInstance(tailoring.rank, int)
        self.assertIsInstance(tailoring.recipes, list)

        self.assertEqual(enchanting.name, Character.JEWELCRATING)

        secondary = character.professions['secondary']

        first_aid = secondary[0]
        archaeology = secondary[1]

        self.assertEqual(first_aid.name, Character.FIRST_AID)
        self.assertEqual(archaeology.name, Character.ARCHAEOLOGY)

    def test_appearance(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Stanislav', fields=[Character.APPEARANCE])

        self.assertEqual(character.appearance.face, 10)
        self.assertEqual(character.appearance.feature, 4)
        self.assertEqual(character.appearance.hair_color, 4)
        self.assertEqual(character.appearance.show_cloak, True)
        self.assertEqual(character.appearance.show_helm, False)
        self.assertEqual(character.appearance.hair, 2)

    def test_lazyload(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Stanislav')

        self.assertEqual(character.guild.realm.name, 'Nazjatar')

    def test_unicode(self):
        character = Character(battlenet.UNITED_STATES, 'Kiljaeden', 'ßæn')

        self.assertEqual(character.name, 'ßæn')

    def test_pet_class(self):
        character = Character(battlenet.UNITED_STATES, 'Kiljaeden', 'Tandisse', fields=[Character.PETS])

        self.assertTrue(hasattr(character, 'pets'))
        self.assertIn('Rudebull', [pet.name for pet in character.pets])

    def test_achievements(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Stanislav', fields=[Character.ACHIEVEMENTS])

        self.assertEqual(character.achievements[513], datetime.datetime(2009, 5, 5, 22, 52, 5))

    def test_progression(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Stanislav', fields=[Character.PROGRESSION])

        for instance in character.progression['raids']:
            if instance.name == 'Blackwing Descent':
                self.assertTrue(instance.is_complete('normal'))

                for boss in instance.bosses:
                    if boss.name == 'Nefarian':
                        self.assertGreater(boss.normal, 0)

    def test_kr_character(self):
        character = Character(battlenet.KOREA, 'Kargath', '내가원조늑인이다')
        self.assertEqual(character.name, '내가원조늑인이다')

if __name__ == '__main__':
    unittest.main()
