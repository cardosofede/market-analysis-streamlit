import streamlit as st
import plotly.express as px

from data.data_provider import DataProvider


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_volume_spreads_df(exchanges):
    data_provider = DataProvider()
    volume_spreads_df = data_provider.get_volume_spreads_df_by_exchange_list(exchanges)
    return volume_spreads_df

def get_exchange_list_filtered(add_miner_exchanges, extra_exchanges, number_of_exchanges, exchange_volume_filter):
    data_provider = DataProvider()
    exchanges = data_provider.exchanges_df
    exchanges_filtered = exchanges[(exchanges["trade_volume_24h_btc"] >= exchange_volume_filter[0]) & (exchanges["trade_volume_24h_btc"] <= exchange_volume_filter[1])].copy()
    exchanges_list = exchanges_filtered["id"].tolist()
    exchanges_list = exchanges_list[:number_of_exchanges]
    if add_miner_exchanges:
        miner_exchanges = data_provider.get_miner_exchanges_id_list()
        for miner_exchange in miner_exchanges:
            exchanges_list.insert(0, miner_exchange)
    if len(extra_exchanges) > 0:
        for exchange in extra_exchanges:
            exchanges_list.append(exchange)
    return exchanges_list

st.set_page_config(layout='wide')
st.title("Market Analysis")
st.write("---")
st.code("This dashboard is using pycoingecko to retrieve information of volume and spread of different markets.")
st.sidebar.write("# Data filters 🏷")
st.sidebar.write("")
data_provider = DataProvider()
volume_spreads_df = None

st.write("")
st.sidebar.write("### Exchange filters 🪙")
with st.sidebar.form(key="market_analysis_filter"):
    exchanges = data_provider.exchanges_df
    add_miner_exchanges = st.checkbox("Add Miner Exchanges", True)
    extra_exchanges = st.multiselect("Extra exchanges to add: ", exchanges["id"])
    st.write("")
    st.write("### Add more exchanges using filters")
    exchange_volume_filter = st.slider("Trade volume BTC filter: ",
                              min_value=exchanges.trade_volume_24h_btc.min().item(),
                              max_value=exchanges.trade_volume_24h_btc.max().item(),
                              value=(exchanges.trade_volume_24h_btc.min().item(), exchanges.trade_volume_24h_btc.max().item()))
    number_of_exchanges = st.slider("Max number of extra filtered exchanges: ", min_value=1, max_value=40, value=11)

    c1, c2 = st.columns([1, 2])
    with c2:
        button = st.form_submit_button("Show me data")

st.sidebar.write("### Token filters 🦅")
miner_token_filter = st.sidebar.checkbox("Miner Token Filter", True)

if volume_spreads_df is None or button:
    exchange_list_filtered = get_exchange_list_filtered(add_miner_exchanges, extra_exchanges, number_of_exchanges, exchange_volume_filter)
    volume_spreads_df = get_volume_spreads_df(exchange_list_filtered)

if miner_token_filter:
    miner_tokens = data_provider.get_miner_base_list()
    volume_spreads_df = volume_spreads_df[volume_spreads_df["base"].isin(miner_tokens)]

spreads = px.scatter(
            volume_spreads_df,
            x="volume",
            y="bid_ask_spread_percentage",
            color="trading_pair",
            log_x=True,
            log_y=True,
            facet_col="exchange",
            facet_col_wrap=3,
            width=1200,
            height=1200,
            template="plotly_dark",
            title="Spread and Volume Chart",
            labels={
                "volume": 'Volume (USD)',
                'bid_ask_spread_percentage': 'Bid Ask Spread (%)'
            })

st.plotly_chart(spreads)
