import os
import pandas as pd
from pathlib import Path
import datetime

# constant string values
directoryName = 'data'
apiKey = '4YDREM9NQ9TXEHYE';
baseRequestString = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&' \
                    'symbol={0}&outputsize={1}&apikey={2}&datatype=csv'

# params: ticker_name and time range(default = ''),
# if time range is 'full': gets all historical data, otherwise gets previous 100 days
# if data already exists, doesn't fetch it again
def fetch_ticker(ticker_name,timerange=''):
    if not Path(pathOfTicker(ticker_name)).exists():
        # default range value
        range = 'compact'

        # if range is 'full', get all historical data
        if timerange == 'full':
            range = 'full'

        # format base string to formatted string with the given params
        formattedAPIUrl = baseRequestString.format(ticker_name, range, apiKey)

        # read csv from the url, using pandas
        tickerDF = pd.read_csv(formattedAPIUrl)

        if check_df_valid(tickerDF):

            # save the data frame to csv file in the data directory
            save_ticker_data_file(ticker_name, tickerDF)
        else:
            raise Exception('Error fetching ticker: ' + ticker_name +', ticker does not exists.')

# returns data for the given ticker_name, time range, data_type (=columns to read)
def get_data_for_ticker_in_range(ticker_name,from_date,to_date, data_type):
    # get path to ticker
    tickerPath = pathOfTicker(ticker_name)

    # if data for the ticker does not exist, fetch it
    if not Path(tickerPath).exists():
        fetch_ticker(ticker_name)

    # read to csv
    tickerDF = pd.read_csv(tickerPath)

    # convert timestamp column to datetime
    tickerDF['timestamp'] = pd.to_datetime(tickerDF['timestamp'])

    # filter rows in the given range
    in_range_df = tickerDF[tickerDF["timestamp"].isin(pd.date_range(from_date, to_date))]

    if in_range_df.empty or not set(data_type).issubset(tickerDF.columns):
        raise Exception('Invalid parameters, or no data in the given range')

    return in_range_df[data_type]


def get_profit_for_ticker_in_range(ticker_name,from_date,to_date,
accumulated=False):
    in_range_df = get_data_for_ticker_in_range(ticker_name, from_date, to_date, ['timestamp', 'close'])
    in_range_df['ticker_name'] = ticker_name.upper()
    in_range_df['daily_profit'] = in_range_df['close'] / in_range_df['close'].shift(1)

    # if accumulated profit is required
    if accumulated:
        in_range_df['daily_profit'] = in_range_df['daily_profit'].cumsum()

    print(in_range_df[['timestamp', 'ticker_name', 'daily_profit']])

    # return only the required columns
    return in_range_df[['timestamp', 'ticker_name', 'daily_profit']]

def get_p2v_for_ticker_in_range(ticker_name,from_date,to_date):
    print()

def save_ticker_data_file(ticker_name, df):
    # creates data directory if not exists
    if not Path(directoryName).exists():
        Path(directoryName).mkdir()

    # save the dataframe as csv to data directory
    df.to_csv(pathOfTicker(ticker_name), index=False)

# return 'data/TICKER_NAME.csv'
def pathOfTicker(ticker_name):
    return os.path.join(directoryName, ticker_name.upper() + '.csv')

# return if dataframe containing error message
def check_df_valid(tickerDF):
    return "Error Message" not in tickerDF.values[0][0]

# 1st func
#fetch_ticker('AAPL')

# 2nd func
day1 = datetime.datetime(2018, 3, 21)
day2 = datetime.datetime(2018, 1, 20)
# get_data_for_ticker_in_range('AAPL', day2, day1, ['close', 'open'])

# 3rd func
get_profit_for_ticker_in_range('AAPL', day2, day1)

