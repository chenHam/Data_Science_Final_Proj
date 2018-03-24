import os
import tickers_data as td

start_date = input('Please enter start date (Format : yyyy-mm-dd) ').upper()
end_date = input('Please enter end date (Format : yyyy-mm-dd) ')
ticker = input('Please enter ticker name ').upper()
path = input('Please enter the path of the file ')
file_name = input('Please enter the name of the file ').upper()
file_type = input('Please enter the format of the file (csv \ json) ').upper()

# for debug
# start_date = '2018-03-20'
# end_date = '2018-03-22'
# ticker = 'msft'
# path = 'C:\\'
# file_name = 'test'
# file_type = 'JSON'

data_type = ['timestamp', 'open', 'high', 'low', 'close', 'volume']


try:
    df = td.get_data_for_ticker_in_range(ticker, start_date, end_date, data_type)
except Exception as e:
    print(str(e))

if not os.path.exists(path):
    print('path not exists, save the file in the local path')
    path = './'
path = os.path.join(path, file_name)

if file_type == 'CSV':
    try:
        df.to_csv(path + '.csv')
        print('save a json file in: ' + path + '.csv')
    except:
        try:
            path = './'
            path = os.path.join(path, file_name)
            df.to_csv(path + '.csv')
            print('path not exists, save the file in the local path')
        except:
            print('cant save a csv file')

if file_type == 'JSON':
    try:
        df.to_json(path + '.json', 'records', True)
        print('save a json file in:' + path + '.json')
    except:
        try:
            path = './'
            path = os.path.join(path, file_name)
            df.to_csv(path + '.json')
            print('path not permitted, save the file in the local path')
        except:
            print('cant save a json file')




