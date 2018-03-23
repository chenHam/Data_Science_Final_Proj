import pandas as pd
from tickers_data import fetch_ticker
from tickers_data import get_data_for_ticker_in_range

# date = input('Please Enter date (Format : yyyy-mm-dd)')
# tickers = input('Please Enter list of tickers').upper()

# for debug:
date = '2018-03-22'
tickers = 'msft,goog'

ticker_date = pd.to_datetime(date)
tickers_list = str.split(tickers, ',')

yesterday = ticker_date + pd.DateOffset(-1)

# for each ticker from list
for ticker in tickers_list:
    try:
        fetch_ticker(ticker)
    except:
        print('The ticker : %s not exists', ticker)
        continue
    data_type = ['timestamp', 'close']
    try:
        df = get_data_for_ticker_in_range(ticker, yesterday, ticker_date, data_type)
    except:
        print('date not exists')

    close_yesterday = df.loc[df['timestamp'] == yesterday, 'close'].values[0]
    close_today = df.loc[df['timestamp'] == ticker_date, 'close'].values[0]

    profit = close_today - close_yesterday

    print("ticker name : {0} , close price : {1} , profit : {2}".format(ticker, str(close_yesterday), str(profit)))

















