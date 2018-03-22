import pandas as pd
import os
from tickers_data import  fetch_ticker
import pandasql as pdsql

# date = input('Please Enter date (Format : yyyy-mm-dd)')
# tickers = input('Please Enter list of tickers')

# for debug:
date = '1990-11-12'
tickers = 'blo,go,fr'

ticker_date = pd.to_datetime(date)
print(str(ticker_date))
tickers_list = str.split(tickers, ',')


# for each ticker from list
for ticker in tickers_list:
    print(ticker)
    fetch_ticker(ticker)

    # read csv file to dataframe
    ticker_file = ticker + '.csv'
    # df = pd.read_csv(os.path.join('data', ticker_file))
    # for debug :
    df = pd.read_csv('goog.csv')

    yesterday = str(ticker_date + pd.DateOffset(-1))
    yesterday_date = yesterday.split(' ')[0]
    # print(yesterday_date)

    query = 'select close from df where timestamp = '
    close_yesterday = pdsql.sqldf(query + yesterday_date)
    close_today = pdsql.sqldf(query + date)
    print(close_yesterday)
    print(close_today)












