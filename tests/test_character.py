# -*- coding: utf-8 -*-

import unittest
import os
import battlenet
import datetime
from battlenet import Character

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)


class CharacterTest(unittest.TestCase):

    _character_name = 'Sejta'
    _region = battlenet.EUROPE
    _realm_name = "Lightning's Blade"
    _guild_name = 'DREAM Paragon'
    _faction = Character.HORDE
    _race = Character.TAUREN
    _class = Character.DRUID
    _level = 85
    _gender = Character.MALE
    _profession_1 = Character.LEATHERWORKING
    _profession_2 = Character.JEWELCRATING
    _professions_secondary = (Character.ARCHAEOLOGY, Character.COOKING, Character.FIRST_AID, Character.FISHING)
    _appearance_face = 1
    _appearance_feature = 6
    _appearance_hair_color = 2
    _appearance_show_cloak = False
    _appearance_show_helm = False
    _appearance_hair = 10

    _character_name_unicode = 'Lappé'
    _character_name_hunter = 'Devai'
    _pet_name = 'DEVAJR'

    _characters = (
        (battlenet.UNITED_STATES, 'illidan', 'Zonker'),
        (battlenet.EUROPE, "Lightning's Blade", 'Sejta'),
        (battlenet.KOREA, '카르가스', '박휘박멸'),
        (battlenet.TAIWAN, '水晶之刺', '憂郁的風'),
    )

    def test_general(self):
        character = Character(self._region, self._realm_name, self._character_name)

        self.assertEqual(character.name, self._character_name)
        self.assertEqual(str(character), self._character_name)

        self.assertEqual(character.get_realm_name(), self._realm_name)
        self.assertEqual(character.realm.name, self._realm_name)
        self.assertEqual(str(character.realm), self._realm_name)

        self.assertEqual(character.faction, self._faction)

        self.assertEqual(character.get_race_name(), self._race)

        self.assertEqual(character.get_class_name(), self._class)

        self.assertIsInstance(character.level, int)
        self.assertGreaterEqual(character.level, 85)

        self.assertIsInstance(character.achievement_points, int)

        self.assertEqual(character.gender, self._gender)

    def test_guild(self):
        character = Character(self._region, self._realm_name, self._character_name, fields=[Character.GUILD])

        self.assertEqual(character.guild.name, self._guild_name)

    def test_stats(self):
        character = Character(self._region, self._realm_name, self._character_name, fields=[Character.STATS])

        self.assertIsInstance(character.stats.agility, int)

    def test_professions(self):
        character = Character(self._region, self._realm_name, self._character_name, fields=[Character.PROFESSIONS])

        primary = character.professions['primary']

        profession_1 = primary[0]
        profession_2 = primary[1]

        self.assertEqual(profession_1.name, self._profession_1)
        self.assertIsInstance(profession_1.rank, int)
        self.assertIsInstance(profession_1.recipes, list)

        self.assertEqual(profession_2.name, self._profession_2)

        secondary = [p.name for p in character.professions['secondary']]

        for p in self._professions_secondary:
            self.assertIn(p, secondary)
        for p in secondary:
            self.assertIn(p, self._professions_secondary)

    def test_appearance(self):
        character = Character(self._region, self._realm_name, self._character_name, fields=[Character.APPEARANCE])

        self.assertEqual(character.appearance.face, self._appearance_face)
        self.assertEqual(character.appearance.feature, self._appearance_feature)
        self.assertEqual(character.appearance.hair_color, self._appearance_hair_color)
        self.assertEqual(character.appearance.show_cloak, self._appearance_show_cloak)
        self.assertEqual(character.appearance.show_helm, self._appearance_show_helm)
        self.assertEqual(character.appearance.hair, self._appearance_hair)

    def test_lazyload(self):
        character = Character(self._region, self._realm_name, self._character_name)

        self.assertEqual(character.guild.realm.name, self._realm_name)

    def test_unicode(self):
        character = Character(self._region, self._realm_name, self._character_name_unicode)

        self.assertEqual(character.name, self._character_name_unicode)

    def test_pet_class(self):
        character = Character(self._region, self._realm_name, self._character_name_hunter, fields=[Character.PETS])

        self.assertTrue(hasattr(character, 'pets'))
        self.assertIn(self._pet_name, [pet.name for pet in character.pets])

    def test_achievements(self):
        character = Character(self._region, self._realm_name, self._character_name, fields=[Character.ACHIEVEMENTS])

        self.assertEqual(character.achievements[513], datetime.datetime(2008, 10, 16, 1, 12, 6))

    def test_progression(self):
        character = Character(self._region, self._realm_name, self._character_name, fields=[Character.PROGRESSION])

        for instance in character.progression['raids']:
            if instance.name == 'Blackwing Descent':
                self.assertTrue(instance.is_complete('normal'))

                for boss in instance.bosses:
                    if boss.name == 'Nefarian':
                        self.assertGreater(boss.normal, 0)

    def test_characters_worldwide(self):
        for region, realm, character_name in self._characters:
            character = Character(region, realm, character_name)
            self.assertEqual(character.name, character_name)

if __name__ == '__main__':
    unittest.main()
