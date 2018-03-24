import tickers_data as td
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import ctir
from ctir import compare_ticks_in_range


# gets time range, tickers and data_type to compare by
def tick_compare(from_date, to_date, ticker_names, data_type):
    # convert to lower case
    data_type = data_type.lower()

    # dataframe that will contain the data for all of tickers
    result_df = pd.DataFrame(columns=['ticker_name', 'timestamp', data_type])

    # foreach ticker
    for ticker in ticker_names:
        try:
            # for the current ticker -

            if data_type in ('close', 'high', 'low'):
                # get the data in range (columns are the given data_type and the timestamp for plot)
                tickerDF = td.get_data_for_ticker_in_range(ticker, from_date, to_date, [data_type, 'timestamp'])
            elif data_type == 'daily_profit':
                tickerDF = td.get_profit_for_ticker_in_range(ticker,from_date, to_date, accumulated=False)
            elif data_type == 'daily_profit_accu':
                tickerDF = td.get_profit_for_ticker_in_range(ticker, from_date, to_date, accumulated=True)

        except Exception as e:
            print(str(e))
            continue

        # add column for the ticker_name and fill it with the current ticker
        tickerDF['ticker_name'] = ticker

        # add tickerDF to the result dataframe
        result_df = result_df.append(tickerDF)

    # plot the result_dataframe
    plot_tickers_df(result_df, data_type)

    # print table comparing tickers using ctir's compare_ticks_in_range function
    compare_ticks_in_range(from_date, to_date, ticker_names)


# gets df containing tickers and field to compare by, draws chart to compare them
def plot_tickers_df(df, data_type):
    # set index for the timestamp
    df = df.set_index('timestamp')

    # group tickers by ticker_name
    grouped = df.groupby(['ticker_name'])
    fig, ax = plt.subplots()

    # plot each group
    for key, group in grouped:
        group[data_type].plot(label=key, ax=ax)

    plt.legend(loc='best')

    # show the chart
    plt.show()

# for debug
end_date = datetime.datetime(2018, 2, 23)
start_date = datetime.datetime(2018, 1, 15)
data_type = 'Daily_profit_accu'
tickers_list = ['MSFT', 'AAPL', 'NVDA', 'AABA']


# start_date = input('Please enter start date (Format : yyyy-mm-dd)')
# end_date = input('Please enter end date (Format : yyyy-mm-dd)')
# tickers = input('Please enter list of tickers (seprated by commas)').upper()
# data_type = input('Please enter one data_type (daily_profit, daily_profit_accu, high, low, close)').lower()
#
# start_date = pd.to_datetime(start_date)
# end_date = pd.to_datetime(end_date)
# tickers = tickers.replace(' ', '')
# tickers_list = str.split(tickers, ',')

tick_compare(start_date, end_date, tickers_list, data_type)
ctir.compare_ticks_in_range(start_date, end_date, tickers_list)

