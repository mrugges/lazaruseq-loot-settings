Spend less time selling and more time farming!

# Core Features

- Automatically mark items to be sold to vendor vs. bazaar 
- Force certain items to always be vendored regardless of bazaar stats
- Force certain items to never be sold to vendor

# Example Workflow

1. Run up to a vendor and run /autosell as usual
2. Wait for macro to finish
3. Run lazarus_loot and note the output (what's bazaarable vs. what's vendor trash)
4. Run /autosell again if output in step 3 looks good
5. (optional) Go to your trader and offload items listed as bazaarable
6. (optional) Update force_vendor.csv with any items that you want to sell to vendor anyway
7. (optional) Update ignore.csv with any items you want to ignore in this process
8. Go back to farming!

# Installation

Run the following commands in your terminal:
- git clone git@github.com:mrugges/lazaruseq-loot-settings.git
- cd lazaruseq-loot-settings
- pip install --editable .

Modify src/config.py to point to the location of your EQ LootSettings.ini
Review force_destroy.csv ignore.csv and force_vendor.csv

Run the following command in your terminal before each /autosell:
- lazarus_loot


