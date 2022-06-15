import time

import pandas as pd
import streamlit as st
import plotly.express as px

from data.data_provider import DataProvider
from utils.coingecko_utils import CoinGeckoUtils
from utils.miner_utils import MinerUtils


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_all_coins_df():
    return CoinGeckoUtils().get_all_coins_df()

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_all_exchanges_df():
    return CoinGeckoUtils().get_all_exchanges_df()

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_miner_stats_df():
    return MinerUtils().get_miner_stats_df()

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_coin_tickers_by_id_list(coins_id: list):
    return CoinGeckoUtils().get_coin_tickers_by_id_list(coins_id)

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_volume_spreads_df(exchanges):
    data_provider = DataProvider()
    volume_spreads_df = data_provider.get_volume_spreads_df_by_exchange_list(exchanges)
    return volume_spreads_df

# def create_spreads_filters(df):
#     miner_coins_filter = st.sidebar.checkbox("Miner Coins")
#     if miener_coins_filter == False:
#         coin_filter = st.sidebar.multiselect("Coins:", df.base.unique().tolist())
#         coins_filters = (df.base_quote.isin(coin_filter)) if len(coin_filter) > 0 else True
#     else:
#         coin_filter = ["ETHUSDT", "BTCUSDT", "USDCUSDT", "LINKUSDT", "WBTCBTC", "DOTUSDT", "VETUSDT", "ADAUSDT", "LTCBTC", "ETHBTC"]
#         coins_filters = df.trading_pair.isin(coin_filter)
#
#     exchange_filter = st.sidebar.multiselect("Exchanges:", df.exchange.unique().tolist())
#     exchanges_filters = (df.exchange.isin(exchange_filter)) if len(exchange_filter) > 0 else True
#
#     spread_filter = st.sidebar.slider(
#         "Spreads:",
#         min_value=float(df.bid_ask_spread_percentage.min()),
#         max_value=float(df.bid_ask_spread_percentage.max()),
#         value=(0.01, 0.8))
#
#     spreads_filters = (df.bid_ask_spread_percentage < spread_filter[1]) & (df.bid_ask_spread_percentage > spread_filter[0])
#     return (spreads_filters & coins_filters & exchanges_filters)
#
# def get_exchange_list_filtered(add_miner_exchanges, extra_exchanges, number_of_exchanges, exchange_volume_filter):
#     data_provider = DataProvider()
#     exchanges = data_provider.exchanges_df
#     exchanges_filtered = exchanges[(exchanges["trade_volume_24h_btc"] >= exchange_volume_filter[0]) & (exchanges["trade_volume_24h_btc"] <= exchange_volume_filter[1])].copy()
#     exchanges_list = exchanges_filtered["id"].tolist()
#     exchanges_list = exchanges_list[:number_of_exchanges]
#     if add_miner_exchanges:
#         miner_exchanges = data_provider.get_miner_exchanges_id_list()
#         for miner_exchange in miner_exchanges:
#             exchanges_list.insert(0, miner_exchange)
#     if len(extra_exchanges) > 0:
#         for exchange in extra_exchanges:
#             exchanges_list.append(exchange)
#     return exchanges_list

st.set_page_config(layout='wide')
st.title("Market Analysis")
st.write("---")
st.code("This dashboard is using pycoingecko to retrieve information of volume and spread of different markets.")
with st.spinner(text='In progress'):
    exchanges_df = get_all_exchanges_df()
    coins_df = get_all_coins_df()
    miner_stats_df = get_miner_stats_df()
    st.success('Done')
miner_coins = coins_df.loc[coins_df["symbol"].isin(miner_stats_df["base"].str.lower().unique()), "name"]
all_miner_coins = ["Algorand", "Avalanche", "DAO Maker", "Faith Tribe", "Fear", "Frontier",
                   "Harmony", "Hot Cross", "HUMAN Protocol", "Oddz", "Shera", "Firo",
                   "Vesper Finance", "Youclout", "Nimiq"]

default_miner_coins = ["Algorand", "Avalanche", "DAO Maker", "HUMAN Protocol", "Harmony", "Frontier"]

st.write("### Coins filter 🦅")
tokens = st.multiselect(
    "Select the tokens to analyze:",
    options=coins_df["name"],
    default=default_miner_coins)

coins_id = coins_df.loc[coins_df["name"].isin(tokens), "id"].tolist()

coin_tickers_df = get_coin_tickers_by_id_list(coins_id)
coin_tickers_df["coin_name"] = coin_tickers_df.apply(lambda x: coins_df.loc[coins_df["id"] == x.coin_id, "name"].item(), axis=1)

with st.expander('Coins data'):
    st.dataframe(coins_df)

with st.expander('Exchanges data'):
    st.dataframe(exchanges_df)

with st.expander('Markets Data'):
    st.dataframe(coin_tickers_df)

fig = px.scatter(
    data_frame=coin_tickers_df,
    x="volume",
    y="bid_ask_spread_percentage",
    color="exchange",
    log_x=True,
    log_y=True,
    facet_col="coin_name",
    facet_col_wrap=3,
    width=1200,
    height=1200,
    template="plotly_dark",
    title="Spread and Volume Chart",
    labels={
        "volume": 'Volume (USD)',
        'bid_ask_spread_percentage': 'Bid Ask Spread (%)'
    })

st.plotly_chart(fig)
st.sidebar.write("# Data filters 🏷")
