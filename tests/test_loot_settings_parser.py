from loot.loot_settings_parser import LootSettingsParser
from pytest import fixture

test_lines = {
    'Fang of Feratha (ND)(L)=Keep': 'Fang of Feratha',
    'Lava Orb (L)=Keep': 'Lava Orb',
    'Tungsten Ore (1000)=Keep': 'Tungsten Ore',
    'Taaffeite 6p(1000)=Keep': 'Taaffeite',
    'Ration 2p5c(1000)=Keep': 'Ration',
    'Refined Grade A Gormar Venom 1c(1000)=Keep': 'Refined Grade A Gormar Venom',
    'Icy Crystal=Keep': 'Icy Crystal',
    '[I]':''
}

@fixture
def parser():
    yield LootSettingsParser()

class TestLootSettingsParser:
    def test_get_item_name(self, parser):
        for item in test_lines:
            res = parser.get_item_name_from_line(item)
            assert res == test_lines[item]

