# -*- coding: utf-8 -*-

import unittest
import os
import battlenet
from battlenet import Character

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)


class CharacterTest(unittest.TestCase):
    def test_general(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy')

        self.assertEqual(character.name, 'Vishnevskiy')
        self.assertEqual(str(character), 'Vishnevskiy')

        self.assertEqual(character.get_realm_name(), 'Nazjatar')
        self.assertEqual(character.realm.name, 'Nazjatar')
        self.assertEqual(str(character.realm), 'Nazjatar')

        self.assertEqual(character.faction, Character.HORDE)

        self.assertEqual(character.get_race_name(), Character.GOBLIN)

        self.assertEqual(character.get_class_name(), Character.WARLOCK)

        self.assertIsInstance(character.level, int)
        self.assertGreaterEqual(character.level, 85)

        self.assertIsInstance(character.achievement_points, int)

        self.assertEqual(character.gender, Character.MALE)

    def test_guild(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy', fields=[Character.GUILD])

        self.assertEqual(character.guild.name, 'Excellence')

    def test_stats(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy', fields=[Character.STATS])

        self.assertIsInstance(character.stats.agility, int)

    def test_professions(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy', fields=[Character.PROFESSIONS])

        primary = character.professions['primary']

        tailoring = primary[0]
        enchanting = primary[1]

        self.assertEqual(tailoring.name, Character.TAILORING)
        self.assertIsInstance(tailoring.rank, int)
        self.assertIsInstance(tailoring.recipes, list)

        self.assertEqual(enchanting.name, Character.ENCHANTING)

        secondary = character.professions['secondary']

        first_aid = secondary[1]
        archaeology = secondary[0]

        self.assertEqual(first_aid.name, Character.FIRST_AID)
        self.assertEqual(archaeology.name, Character.ARCHAEOLOGY)

    def test_appearance(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy', fields=[Character.APPEARANCE])

        self.assertEqual(character.appearance.face, 2)
        self.assertEqual(character.appearance.feature, 9)
        self.assertEqual(character.appearance.hair_color, 3)
        self.assertEqual(character.appearance.show_cloak, True)
        self.assertEqual(character.appearance.show_helm, True)
        self.assertEqual(character.appearance.hair, 5)

    def test_lazyload(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy')

        self.assertEqual(character.guild.realm.name, 'Nazjatar')

    def test_unicode(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Clí')

        self.assertEqual(character.name, 'Clí')

    def test_pet_class(self):
        character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Tandisse', fields=[Character.PETS])

        self.assertTrue(hasattr(character, 'pets'))
        self.assertIn('Rudebull', [pet.name for pet in character.pets])

    def test_eu_character(self):
        character = Character(battlenet.EUROPE, 'свежеватель-душ', 'Поникс')
        self.assertEqual(character.name, 'Поникс')

if __name__ == '__main__':
    unittest.main()
