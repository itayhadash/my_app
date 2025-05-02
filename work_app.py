import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit.runtime.scriptrunner import add_script_run_ctx
import financedatabase as fd

st.title("Finance Analysis App")

sp500_tickers = list(pd.Series(list(set(fd.Equities().select().index).union(set(fd.ETFs().select().index)))).dropna().values)
select_name = st.selectbox("select S&P 500 stock",sp500_tickers)
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
    con.line_chart(historical_data, x="Date", y="Close")
else:
    None



