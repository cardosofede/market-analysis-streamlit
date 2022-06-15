import pandas as pd


class DataProvider:

    def __init__(self,
                 miner_stats_df: pd.DataFrame,
                 exchanges_df: pd.DataFrame,
                 coins_df: pd.DataFrame,
                 coins_tickers_df: pd.DataFrame):
        self._miner_stats_df = miner_stats_df
        self._exchanges_df = exchanges_df
        self._coins_df = coins_df
        self._coins_tickers_df = coins_tickers_df

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

    # def get_top_exchanges_spreads_by_volume(self, top: int = 40):
    #     dfs = []
    #     exchanges = self._exchanges_df
    #     top_exchanges_id = exchanges.loc[:top, "id"]
    #     for exchange_id in top_exchanges_id:
    #         df = pd.DataFrame(self.connector.get_exchanges_by_id(exchange_id)["tickers"])
    #         dfs.append(df)
    #     exchanges_spreads_df = pd.concat(dfs)
    #     exchanges_spreads_df["exchange"] = exchanges_spreads_df["market"].apply(lambda x: re.sub("Exchange", "", x["name"]))
    #     exchanges_spreads_df.drop(columns="market", inplace=True)
    #     exchanges_spreads_df["trading_pair"] = exchanges_spreads_df.base + "-" + exchanges_spreads_df.target
    #     return exchanges_spreads_df

