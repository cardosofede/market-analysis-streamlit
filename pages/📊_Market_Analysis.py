import streamlit as st
import plotly.express as px

from data.data_provider import DataProvider


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_volume_spreads_df(exchanges):
    data_provider = DataProvider()
    volume_spreads_df = data_provider.get_volume_spreads_df_by_exchange_list(exchanges)
    return volume_spreads_df

def create_spreads_filters(df):
    miner_coins_filter = st.sidebar.checkbox("Miner Coins")
    if miener_coins_filter == False:
        coin_filter = st.sidebar.multiselect("Coins:", df.base.unique().tolist())
        coins_filters = (df.base_quote.isin(coin_filter)) if len(coin_filter) > 0 else True
    else:
        coin_filter = ["ETHUSDT", "BTCUSDT", "USDCUSDT", "LINKUSDT", "WBTCBTC", "DOTUSDT", "VETUSDT", "ADAUSDT", "LTCBTC", "ETHBTC"]
        coins_filters = df.trading_pair.isin(coin_filter)

    exchange_filter = st.sidebar.multiselect("Exchanges:", df.exchange.unique().tolist())
    exchanges_filters = (df.exchange.isin(exchange_filter)) if len(exchange_filter) > 0 else True
    
    spread_filter = st.sidebar.slider(
        "Spreads:",
        min_value=float(df.bid_ask_spread_percentage.min()), 
        max_value=float(df.bid_ask_spread_percentage.max()),
        value=(0.01, 0.8))
    
    spreads_filters = (df.bid_ask_spread_percentage < spread_filter[1]) & (df.bid_ask_spread_percentage > spread_filter[0])
    return (spreads_filters & coins_filters & exchanges_filters)

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
st.sidebar.write("### Miner filters 🦅")
miner_token_filter = st.sidebar.checkbox("Miner Token Filter", True)

with st.sidebar.form(key="market_analysis_filter"):
    exchanges = data_provider.exchanges_df
    st.write("")
    st.write("### Exchange filters 🪙")
    add_miner_exchanges = st.checkbox("Add Miner Exchanges", True)
    extra_exchanges = st.multiselect("Extra exchanges to add: ", exchanges["id"])
    st.write("---")

    st.write("### Add more exchanges using filters")
    exchange_volume_filter = st.slider("Trade volume BTC filter: ",
                              min_value=exchanges.trade_volume_24h_btc.min().item(),
                              max_value=exchanges.trade_volume_24h_btc.max().item(),
                              value=(exchanges.trade_volume_24h_btc.min().item(), exchanges.trade_volume_24h_btc.max().item()))
    number_of_exchanges = st.slider("Max number of extra filtered exchanges: ", min_value=1, max_value=40, value=11)

    c1, c2 = st.columns([1, 2])
    with c2:
        button = st.form_submit_button("Show me data")

exchange_list_filtered = get_exchange_list_filtered(add_miner_exchanges, extra_exchanges, number_of_exchanges, exchange_volume_filter)
volume_spreads_df = get_volume_spreads_df(exchange_list_filtered)

if miner_token_filter:
    miner_tokens = data_provider.get_miner_base_list()
    volume_spreads_df = volume_spreads_df[volume_spreads_df["base"].isin(miner_tokens)]

spreads = px.scatter(
            volume_spreads_df,
            y="bid_ask_spread_percentage",
            x="volume",
            color="trading_pair",
            log_x=True,
            log_y=True,
            facet_col="exchange",
            facet_col_wrap=3,
            hover_data=["base", "target"],
            width=1200,
            height=800,
            template="plotly_dark",
            title="Spread and Volume Chart",
            labels={
                "x":'Volume',
                'y':'Spread'
            })

st.plotly_chart(spreads)
