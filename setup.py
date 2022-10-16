from distutils.core import setup

setup(
    name='LazarusLoot',
    version='0.2.3',
    packages=['src',],
    py_modules=['lazarus_loot', 'loot_settings_parser'],
    install_requires=[
        'Click', 'pandas'
    ],
    entry_points={
        'console_scripts': [
            'lazarus_loot = src.lazarus_loot:cli',
        ],
    },
    package_data={'lazarus_loot': ['*.csv']},
    include_package_data=False,
)
