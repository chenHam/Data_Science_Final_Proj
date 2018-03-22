import pandas as pd
from sqlalchemy.sql.operators import from_
import datetime

import tickers_data as td



def compare_ticks_in_range(from_date, to_date, ticker_names):
    result_list = []

    for ticker in ticker_names:
        in_range_df = td.get_data_for_ticker_in_range(ticker, from_date, to_date, ['close'])
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

    print('result')
    print(result_df)

day1 = datetime.datetime(2018, 3, 21)
day2 = datetime.datetime(2018, 1, 20)
compare_ticks_in_range(day2, day1, ['MSFT', 'AAPL'])