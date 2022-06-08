from utils.coingecko_utils import CoinGeckoUtils
from utils.miner_utils import MinerUtils


class DataProvider:
    def __init__(self):
        self._miner_utils = MinerUtils()
        self._cg_utils = CoinGeckoUtils()
        self._miner_stats_df = self._miner_utils.get_miner_stats_df()
        self._exchanges_df = self._cg_utils.get_all_exchanges_df()
        self._trading_pairs_df = self._cg_utils.get_all_coins_df()

    @property
    def exchanges_df(self):
        return self._exchanges_df

    def get_miner_exchanges_id_list(self):
        miner_exchanges = self._miner_stats_df["coingecko_id"].unique().tolist()
        return miner_exchanges

    def get_miner_base_list(self):
        miner_trading_pairs = self._miner_stats_df["base"].unique().tolist()
        return miner_trading_pairs

    def get_all_exchanges_name_list(self):
        self._exchanges_df["id"].unique().tolist()

    def get_all_base_list(self):
        self._exchanges_df["base"].unique().tolist()

    def get_exchanges_filtered_by_miner(self):
        return self._exchanges_df[self._exchanges_df["id"].isin(self.get_miner_exchanges_id_list())]

    def get_trading_pairs_filtered_by_miner(self):
        return self._exchanges_df[self._exchanges_df["trading_pairs"].isin(self.get_trading_pairs_filtered_by_miner())]

    def get_volume_spreads_df_by_exchange_list(self, exchange: list):
        exchanges_markets_info = self._cg_utils.get_exchanges_markets_info_by_list(exchange)
        volume_spread_df = exchanges_markets_info[["base", "target", "volume", "bid_ask_spread_percentage", "exchange", "trading_pair"]].copy()
        return volume_spread_df

