import pandas as pd
from datetime import datetime, timedelta
import tickers_data as td

# date = input('Please Enter date (Format : yyyy-mm-dd)')
# tickers = input('Please Enter list of tickers (seprated by commas) ').upper()

# for debug:
date = '2018-03-22'
tickers = 'msft,goog   ,7658'

ticker_date = pd.to_datetime(date)
tickers = tickers.replace(' ', '')
tickers_list = str.split(tickers, ',')

yesterday = ticker_date + pd.DateOffset(-1)
date_100_days_ago = datetime.now() - timedelta(100)

timerange = None
if ticker_date < date_100_days_ago:
    timerange = 'full'

# for each ticker from list
for ticker in tickers_list:

    try:
        td.fetch_ticker(ticker, timerange)
    except Exception as e:
        print(str(e))
        continue

    data_type = ['timestamp', 'close']

    try:
        df = td.get_data_for_ticker_in_range(ticker, yesterday, ticker_date, data_type)
    except Exception as e:
        print(str(e))
        continue

    close_yesterday = df.loc[df['timestamp'] == yesterday, 'close'].values[0]
    close_today = df.loc[df['timestamp'] == ticker_date, 'close'].values[0]

    profit = close_today - close_yesterday

    print("ticker name : {0} , close price : {1} , profit : {2}".format(ticker, str(close_yesterday), str(profit)))

















