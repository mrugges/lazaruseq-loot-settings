import re
import pandas as pd
import fileinput
import logging
from src.config import eq


class LootSettingsParser:
    def __init__(self):
        self.item_stat_col_to_filter = "avg_30d"
        self.loot_settings_path = eq["loot_settings_path"]
        # how much higher should bazaar historical average price
        # be over vendor price to not be considered vendor trash
        self.pct_over_hist_average = 0.5
        self.ignore_set = set(pd.read_csv("ignore.csv")["name"])
        self.destroy_set = set(pd.read_csv("force_destroy.csv")["name"])
        self.loot_items = []
        self.price_pattern = re.compile("([0-9]+p)*([0-9]+s)*([0-9]+c)*")
        self.line_pattern = re.compile(
            "(\[[A-Z]{1}\])|(([A-z ;'-]+)(\(ND\)){0,1}(\(L\)){0,1}([0-9]+p){0,1}([0-9]+g){0,1}([0-9]+s){0,1}([0-9]+c){0,1}(\([0-9]+\)){0,1}(\(L\)){0,1}=(Keep|Sell|Destroy|Skip)([|][0-9]+){0,1})"
        )
        self.bazaarable = []

    def clean_name(self, n):
        return n.rstrip().replace(";", ":") if n else ""

    def run(self):
        logging.info(
            "Welcome to Lazarus Project Loot Settings Parser."
            " Please report any warnings or issues at https://github.com/mrugges/lazaruseq-loot-settings/issues/new"
        )

        with open(self.loot_settings_path) as f:

            for line_number, line in enumerate(f):
                # logging.info(f"{line_number} {line}")
                matches = self.line_pattern.match(line)
                if not matches:
                    logging.warning("unexpected line, check regexp for:")
                    logging.warning(line)
                    continue

                if matches.group(1):
                    continue

                item_name = self.clean_name(matches.group(3))

                if matches.group(6):

                    full_price = matches.group(6)

                    plat_price = "0"
                    if "p" in full_price:
                        plat_price = full_price[: full_price.index("p")]

                    self.loot_items += [[item_name, int(plat_price), line_number]]
                else:
                    self.loot_items += [[item_name, 0, line_number]]

        vendor_prices = pd.DataFrame(self.loot_items)

        if not vendor_prices.size:
            print(f"Please check Loot Settings file at {self.loot_settings_path}")
            exit(1)

        vendor_prices.columns = ["name", "vendor_price", "line_number"]

        item_stats = pd.read_csv("item_stats.csv")

        vs = vendor_prices.join(item_stats.set_index("name"), on="name")
        vs.fillna(0, inplace=True)

        force_vendor_names = pd.read_csv("force_vendor.csv")

        price_filter = (
            (vs[self.item_stat_col_to_filter] < 50)
            | (vs["vendor_price"] >= vs[self.item_stat_col_to_filter])
            | vs["name"].isin(force_vendor_names["name"])
        ) & ~vs["name"].isin(self.ignore_set)

        vendor_trash = vs.where(price_filter).dropna()

        logging.info("vendor trash:")
        logging.info(vendor_trash)

        self.bazaarable = vs.where(
            ~vs["name"].isin(vendor_trash["name"]) & ~vs["name"].isin(self.ignore_set)
        ).dropna()

        # vs.where(
        # (vs['hist_avg_price'] > vs['vendor_price'] + vs['vendor_price'] * pct_over_hist_average)
        # & ~vs['name'].isin(force_vendor_names['name']) & vs['hist_avg_price'] > 50

        logging.info("bazaarable, give it to a trader and run bazaar.py:")
        baz_ord = self.bazaarable[
            ["name", "vendor_price", self.item_stat_col_to_filter]
        ].sort_values(by=self.item_stat_col_to_filter, ascending=False)
        logging.info(baz_ord)
        baz_ord.to_csv("bazaarable.log", sep="\t")

        destroying = self.process_vendor_trash(vendor_trash)
        logging.info("set to destroy:")
        logging.info(destroying)

    def get_item_name_from_line(self, ln):
        m = self.line_pattern.match(ln)
        return self.clean_name(m.group(3)) if m else ""

    # print(vs.drop(columns='vendor_price'))

    def set_to(self, full_line: str, v: str) -> str:
        """
        :param full_line: line
        :param v: Sell / Keep / Destroy
        :return:
        """
        left, right = full_line.split("=")
        return f"{left}={v}"

    def process_vendor_trash(self, vendor_trash):
        vendor_trash_set = set(vendor_trash["line_number"])
        bazaarable_set = set(self.bazaarable["name"])
        # print(vendor_trash_set)
        set_to_destroy = []
        for line_number, line in enumerate(
            fileinput.input(self.loot_settings_path, inplace=True)
        ):
            item_name = self.get_item_name_from_line(line)
            if line_number in vendor_trash_set:
                print(self.set_to(line, "Sell"))
            elif item_name in self.ignore_set:
                print(self.set_to(line, "Keep"))
            elif item_name in self.destroy_set:
                print(self.set_to(line, "Destroy"))
                set_to_destroy += [item_name]
            elif item_name in bazaarable_set:
                print(self.set_to(line, "Keep"))
            else:
                print(line, end="")

        print("updated loot settings.ini with vendor trash")
        return set_to_destroy
