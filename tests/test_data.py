import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest as unittest
import os
import battlenet
from operator import itemgetter

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

class DataTest(unittest.TestCase):
    def setUp(self):
        self.connection = battlenet.Connection(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

    def test_races(self):
        races = self.connection.get_character_races(
            battlenet.UNITED_STATES, raw=True)

        self.assertEqual(races, [
                {'mask': 4, 'id': 3, 'name': 'Dwarf', 'side': 'alliance'},
                {'mask': 32, 'id': 6, 'name': 'Tauren', 'side': 'horde'},
                {'mask': 16, 'id': 5, 'name': 'Undead', 'side': 'horde'},
                {'mask': 2, 'id': 2, 'name': 'Orc', 'side': 'horde'},
                {'mask': 64, 'id': 7, 'name': 'Gnome', 'side': 'alliance'},
                {'mask': 128, 'id': 8, 'name': 'Troll', 'side': 'horde'},
                {'mask': 256, 'id': 9, 'name': 'Goblin', 'side': 'horde'},
                {'mask': 1024, 'id': 11, 'name': 'Draenei', 'side': 'alliance'},
                {'mask': 2097152, 'id': 22, 'name': 'Worgen', 'side': 'alliance'},
                {'mask': 512, 'id': 10, 'name': 'Blood Elf', 'side': 'horde'},
                {'mask': 1, 'id': 1, 'name': 'Human', 'side': 'alliance'},
                {'mask': 8, 'id': 4, 'name': 'Night Elf', 'side': 'alliance'}
        ])

        races = self.connection.get_character_races(battlenet.UNITED_STATES)

        for race in races:
            self.assertIn(race.side, ['alliance', 'horde'])

    def test_classes(self):
        classes = self.connection.get_character_classes(
            battlenet.UNITED_STATES, raw=True)

        classes_ = [
                {'powerType': 'focus', 'mask': 4, 'id': 3, 'name': 'Hunter'},
                {'powerType': 'rage', 'mask': 1, 'id': 1, 'name': 'Warrior'},
                {'powerType': 'mana', 'mask': 16, 'id': 5, 'name': 'Priest'},
                {'powerType': 'mana', 'mask': 256, 'id': 9, 'name': 'Warlock'},
                {'powerType': 'mana', 'mask': 64, 'id': 7, 'name': 'Shaman'},
                {'powerType': 'mana', 'mask': 2, 'id': 2, 'name': 'Paladin'},
                {'powerType': 'energy', 'mask': 8, 'id': 4, 'name': 'Rogue'},
                {'powerType': 'runic-power', 'mask': 32, 'id': 6, 'name': 'Death Knight'},
                {'powerType': 'mana', 'mask': 1024, 'id': 11, 'name': 'Druid'},
                {'powerType': 'mana', 'mask': 128, 'id': 8, 'name': 'Mage'}
        ]

        classes_.sort(key=itemgetter('id'))
        classes.sort(key=itemgetter('id'))

        self.assertEqual(classes, classes_)

        classes = self.connection.get_character_classes(battlenet.UNITED_STATES)

        for class_ in classes:
            self.assertIn(class_.power_type,
                ['mana', 'energy', 'runic-power', 'focus', 'rage'])

    def test_items(self):
        item = self.connection.get_item(battlenet.UNITED_STATES, 60249)
        # TODO

if __name__ == '__main__':
    unittest.main()
