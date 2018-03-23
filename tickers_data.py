import os
import pandas as pd
from pathlib import Path
import numpy as np

# constant string values
directoryName = 'data'
apiKey = '4YDREM9NQ9TXEHYE';
baseRequestString = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&' \
                    'symbol={0}&outputsize={1}&apikey={2}&datatype=csv'


# params: ticker_name and time range(default = ''),
# if time range is 'full': gets all historical data, otherwise gets previous 100 days
# if data already exists, doesn't fetch it again
def fetch_ticker(ticker_name, timerange=''):
    if not Path(pathOfTicker(ticker_name)).exists():
        # default range value
        range = 'compact'

        # if range is 'full', get all historical data
        if timerange == 'full':
            range = 'full'

        # format base string to formatted string with the given params
        formatted_api_url = baseRequestString.format(ticker_name, range, apiKey)

        # read csv from the url, using pandas
        ticker_df = pd.read_csv(formatted_api_url)

        if check_df_valid(ticker_df):

            # save the data frame to csv file in the data directory
            save_ticker_data_file(ticker_name, ticker_df)
        else:
            raise Exception('Error fetching ticker: ' + ticker_name +', ticker does not exists.')


# returns data for the given ticker_name, time range, data_type (=columns to read)
def get_data_for_ticker_in_range(ticker_name, from_date_str, to_date_str, data_type):

    # try converting dates to datetime type, raise exception on failure
    try:
        from_date = pd.to_datetime(from_date_str)
        to_date = pd.to_datetime(to_date_str)
    except ValueError:
        raise Exception('Invalid date or date format')

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


def get_profit_for_ticker_in_range(ticker_name, from_date_str, to_date_str, accumulated=False):
    # try converting dates to datetime type, raise exception on failure
    try:
        from_date = pd.to_datetime(from_date_str)
        to_date = pd.to_datetime(to_date_str)
    except ValueError:
        raise Exception('Invalid date or date format')

    # gets data for the given ticker in the given range
    in_range_df = get_data_for_ticker_in_range(ticker_name, from_date, to_date, ['timestamp', 'close'])

    # create column 'ticker_name' containing the given ticker_name
    in_range_df['ticker_name'] = ticker_name.upper()

    # calculates the daily profit by using another df with shift(1)
    in_range_df['daily_profit'] = in_range_df['close'] / in_range_df['close'].shift(1)

    # if accumulated profit is required
    if accumulated:
        in_range_df['daily_profit'] = in_range_df['daily_profit'].cumsum()

    # returns only the required columns
    return in_range_df[['timestamp', 'ticker_name', 'daily_profit']]

# params: ticker_name, time range
# return: peak_to_valley, peak, valley
def get_p2v_for_ticker_in_range(ticker_name, from_date, to_date):

    # get data in range for the given ticker
    in_range_df = get_data_for_ticker_in_range(ticker_name, from_date, to_date, ['timestamp', 'close'])

    # find peak value for 'close' field
    peak_close = in_range_df['close'].max()

    # find the index of the peak
    peak_close_idx = in_range_df['close'].idxmax()

    # remove all rows after the peak index
    after_peak_df = in_range_df[:peak_close_idx+1]

    # find the valley (minimal closing value) after the peak
    valley_close = after_peak_df['close'].min()

    # find the index of the valley
    valley_close_idx = after_peak_df['close'].idxmin()

    # calculates the day difference between the peak and the valley
    valley_date = after_peak_df['timestamp'].values[valley_close_idx]
    peak_date = after_peak_df['timestamp'].values[peak_close_idx]

    # convert datetimedelta to days integer
    day_diff = (valley_date - peak_date) / np.timedelta64(1, 'D')

    # calculates the difference in value of the peak and the valley
    peak_to_valley = peak_close - valley_close

    # return the calculated values
    return peak_to_valley, peak_close, valley_close, day_diff

# gets ticker_name and dataframe
# creates a csv file with the ticker_name from the data frame
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
# day1 = '2018-03-25'
# day2 = '2018-01-01'
# get_data_for_ticker_in_range('AAPL', day2, day1, ['close', 'open'])

# 3rd func
# get_profit_for_ticker_in_range('AAPL', day2, day1)

# 4th func
# get_p2v_for_ticker_in_range('GOOG', day2, day1)

