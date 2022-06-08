import unittest

import pandas as pd

from utils.coingecko_utils import CoinGeckoUtils


class CoinGeckoUtilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cg = CoinGeckoUtils()

    def test_get_all_coins(self):
        coins = self.cg.get_all_coins_df()
        self.assertEqual(type(coins), pd.DataFrame)

    def test_get_all_exchanges(self):
        exchanges = self.cg.get_all_exchanges_df()
        self.assertEqual(type(exchanges), pd.DataFrame)

    def test_get_exchanges_spreads(self):
        exchanges_spreads = self.cg.get_top_exchanges_spreads_by_volume(top=3)
        self.assertEqual(type(exchanges_spreads), pd.DataFrame)

    def test_get_exchanges_spreads_by_list(self):
        exchanges_spreads = self.cg.get_exchanges_markets_info_by_list(["binance"])
        self.assertEqual(type(exchanges_spreads), pd.DataFrame)


