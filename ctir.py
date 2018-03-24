import pandas as pd
import tickers_data as td


def compare_ticks_in_range(from_date, to_date, ticker_names):
    result_list = []

    for ticker in ticker_names:
        try:
            in_range_df = td.get_data_for_ticker_in_range(ticker, from_date, to_date, ['close'])
        except Exception as e:
            print(str(e))
            continue

        total_profit = in_range_df['close'].head(1).values[0] - in_range_df['close'].tail(1).values[0]

        peak_to_valley, peak, valley, day_diff = td.get_p2v_for_ticker_in_range(ticker, from_date, to_date)
        mean = in_range_df['close'].mean()
        standard_deviation = in_range_df['close'].std()

        result_list.append({
            'ticker_name': ticker,
            'total_profit': total_profit,
            'peak_to_valley': peak_to_valley,
            'peak': peak,
            'valley': valley,
            'mean': mean,
            'standard_deviation': standard_deviation
        })

    result_df = pd.DataFrame(result_list, columns=['ticker_name',
                                      'total_profit',
                                      'peak_to_valley',
                                      'peak', 'valley',
                                      'mean',
                                      'standard_deviation'])

    print('result:')
    if result_df.empty:
        print('There in no result for the given parameters')
    else:
        print(result_df)


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here

    # for debug
    # start_date = datetime.datetime(2018, 1, 20)
    # end_date = datetime.datetime(2018, 3, 21)
    # tickers_list = ['MSFT', 'AAPL']

    start_date = input('Please enter start date (Format : yyyy-mm-dd)')
    end_date = input('Please enter end date (Format : yyyy-mm-dd)')
    tickers = input('Please enter list of tickers(seprated by commas) ').upper()

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    tickers = tickers.replace(' ', '')
    tickers_list = str.split(tickers, ',')

    compare_ticks_in_range(start_date, end_date, tickers_list)


