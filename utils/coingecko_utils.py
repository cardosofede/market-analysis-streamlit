from pycoingecko import CoinGeckoAPI
import pandas as pd
import re


class CoinGeckoUtils:
    def __init__(self):
        self.connector = CoinGeckoAPI()

    def get_all_coins_df(self):
        coin_list = self.connector.get_coins_list()
        return pd.DataFrame(coin_list)

    def get_all_exchanges_df(self):
        exchanges_list = self.connector.get_exchanges_list()
        return pd.DataFrame(exchanges_list)

    def get_top_exchanges_spreads_by_volume(self, top: int = 40):
        dfs = []
        exchanges = self.get_all_exchanges_df()
        top_exchanges_id = exchanges.loc[:top, "id"]
        for exchange_id in top_exchanges_id:
            df = pd.DataFrame(self.connector.get_exchanges_by_id(exchange_id)["tickers"])
            dfs.append(df)
        exchanges_spreads_df = pd.concat(dfs)
        exchanges_spreads_df["exchange"] = exchanges_spreads_df["market"].apply(lambda x: re.sub("Exchange", "", x["name"]))
        exchanges_spreads_df.drop(columns="market", inplace=True)
        exchanges_spreads_df["trading_pair"] = exchanges_spreads_df.base + "-" + exchanges_spreads_df.target
        return exchanges_spreads_df

    def get_exchanges_markets_info_by_list(self, exchanges_id: list):
        dfs = []
        for exchange_id in exchanges_id:
            df = pd.DataFrame(self.connector.get_exchanges_by_id(exchange_id)["tickers"])
            dfs.append(df)
        exchanges_spreads_df = pd.concat(dfs)
        exchanges_spreads_df["exchange"] = exchanges_spreads_df["market"].apply(
            lambda x: re.sub("Exchange", "", x["name"]))
        exchanges_spreads_df.drop(columns="market", inplace=True)
        exchanges_spreads_df["trading_pair"] = exchanges_spreads_df.base + "-" + exchanges_spreads_df.target
        return exchanges_spreads_df

