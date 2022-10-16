from distutils.core import setup

setup(
    name='LazarusLoot',
    version='0.1dev',
    packages=['src',],
    long_description=open('Readme.md').read(),
    py_modules=['lazarus_loot', 'loot_settings_parser'],
    install_requires=[
        'Click', 'pandas'
    ],
    entry_points={
        'console_scripts': [
            'lazarus_loot = src.lazarus_loot:cli',
        ],
    },
)
