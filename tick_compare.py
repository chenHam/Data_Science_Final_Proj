import tickers_data as td
import datetime
import pandas as pd
import matplotlib.pyplot as plt


def tick_compare(from_date, to_date, ticker_names, data_type):
    result_df = pd.DataFrame(columns=['ticker_name', 'timestamp', data_type])

    for ticker in ticker_names:
        try:
            ticker_df = td.get_data_for_ticker_in_range(ticker, from_date, to_date, [data_type, 'timestamp'])
        except Exception as e:
            print(str(e))
            continue

        ticker_df = ticker_df[['timestamp', data_type]]
        ticker_df['ticker_name'] = ticker

        result_df = result_df.append(ticker_df)

    print(result_df)

    plot_tickers_df(result_df)

    result_df.plot(x='timestamp', y='close')


def plot_tickers_df(df):
    df = df.set_index('timestamp')
    grouped = df.groupby(['ticker_name'])
    fig, ax = plt.subplots()

    for key, group in grouped:
        group['close'].plot(label=key, ax=ax)

    plt.legend(loc='best')

    plt.show()


# for debug
end_date = datetime.datetime(2018, 3, 21)
start_date = datetime.datetime(2018, 1, 20)
data_type = 'close'
tickers_list = ['MSFT', 'AAPL', 'GOOG']

# start_date = input('Please enter start date (Format : yyyy-mm-dd)')
# end_date = input('Please enter end date (Format : yyyy-mm-dd)')
# tickers = input('Please enter list of tickers (seprated by commas)').upper()
# data_type = input('Please enter one data_type (timestamp,open,high,low,close,volume)').upper()
#
# start_date = pd.to_datetime(start_date)
# end_date = pd.to_datetime(end_date)
# tickers_list = str.split(tickers, ',')

tick_compare(start_date, end_date, tickers_list, data_type)

