import unittest

import pandas as pd

from utils.miner_utils import MinerUtils


class MinerUtilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.miner = MinerUtils()

    def test_get_miner_stats_df(self):
        miner_stats = self.miner.get_miner_stats_df()
        self.assertEqual(type(miner_stats), pd.DataFrame)

    def test_get_miner_exchanges_list(self):
        exchange_list = self.miner.get_miner_exchanges_list()
        self.assertEqual(type(exchange_list), list)

    def test_get_miner_trading_pairs_list(self):
        trading_pairs_list = self.miner.get_miner_trading_pairs_list()
        self.assertEqual(type(trading_pairs_list), list)
