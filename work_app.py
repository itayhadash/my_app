import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit.runtime.scriptrunner import add_script_run_ctx
import financedatabase as fd

st.title("Finance Analysis App")
@st.cache_data
def load_tic():
    sp500_df = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    sp500_tickers = sp500_df['Symbol'].tolist()
    sp500_tickers = [ticker.replace('.', '-') for ticker in sp500_tickers]

    return sp500_tickers


sp500_tickers = load_tic()

select_name = st.selectbox("select stock",sp500_tickers)
st.write(fd.Equities().select().query("symbol==@select_name").name.values[0])
select_period = st.selectbox('select_period',['1mo','1d','1w','1y'])
select_interval = st.selectbox('select_interval',['1mo','1d','1w','1y'])
execute = st.button("execute")
ticker = yf.Ticker(select_name)

# Fetch historical market data
if execute:
    historical_data = ticker.history(period=select_period,interval=select_interval)  # data for the last year
    st.write("Data")
    historical_data=historical_data.reset_index()
    st.write(pd.DataFrame(historical_data))

    col1, col2, col3,col4= st.columns(4,vertical_alignment='center')
    col1.metric("Start", str((round(historical_data.Open[0])))+"$")
    col2.metric("High",str(round(max(historical_data.High)))+"$")
    col3.metric("Low",str(round(min(historical_data.Low)))+"$")
    col4.metric("End", str((round(historical_data.Open[historical_data.shape[0]-1]))) + "$")

    con = st.container(border=True)
    con.line_chart(historical_data, x="Date", y="Close",x_label="Date", y_label='Close price')

else:
    None



