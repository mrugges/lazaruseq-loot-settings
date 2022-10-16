import click
from src.loot_settings_parser import LootSettingsParser
import logging
import sys


@click.command()
def cli():


    logging.basicConfig(
        handlers=[
            logging.FileHandler('lazarus_loot.log'), logging.StreamHandler(sys.stdout)
        ],
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )



    LootSettingsParser().run()
