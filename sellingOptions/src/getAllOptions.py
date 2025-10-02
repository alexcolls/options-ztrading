from src.apis.polygonApi import api_key
from tabulate import tabulate
from sys import getsizeof
import pandas as pd
import requests
import csv

file = open('src/apis/db/tickers.csv', 'r')
tickers = list(csv.reader(file, delimiter=","))[0]

# get option chain
limit = 250
contract = 'call'
expiration = '2023-01-20'
history = pd.DataFrame(columns=['ticker', 'ticker_option', 'contract_type', 'exercise_style', 'expiration_date', 'close', 'volume', 'vwap', 'breakeven',
                       'volatility', 'open_interest', 'strike_price', 'ask', 'ask_size', 'bid', 'bid_size', 'underlying_price', 'distance', 'distance_percent'])

for ticker in tickers:
    print(ticker)
    endpoint = 'https://api.polygon.io/v3/snapshot/options/'+ticker+'?expiration_date=' + \
        expiration+'&contract_type='+contract + \
        '&limit='+str(limit)+'&apiKey='+str(api_key)
    res = requests.get(endpoint)
    # if res.status_code == 200:
    data = res.json()
    for x in data['results']:
        try:
            ticker = x['underlying_asset']['ticker']
            ticker_option = x['details']['ticker']
            contract_type = x['details']['contract_type']
            exercise_style = x['details']['exercise_style']
            expiration_date = x['details']['expiration_date']
            close = x['day']['close']
            volume = x['day']['volume']
            vwap = x['day']['vwap']
            breakeven = x['break_even_price']
            volatility = x['implied_volatility']
            open_interest = x['open_interest']
            strike_price = x['details']['strike_price']
            ask = x['last_quote']['ask']
            ask_size = x['last_quote']['ask_size']
            bid = x['last_quote']['bid']
            bid_size = x['last_quote']['bid_size']
            underlying_price = x['underlying_asset']['price']
            distance = strike_price - underlying_price
            distance_percent = round(
                ((strike_price / underlying_price - 1) * 100), 2)
            row = {
                'ticker': ticker,
                'ticker_option': ticker_option,
                'contract_type': contract_type,
                'exercise_style': exercise_style,
                'expiration_date': expiration_date,
                'close': close,
                'volume': volume,
                'vwap': vwap,
                'breakeven': breakeven,
                'volatility': volatility,
                'open_interest': open_interest,
                'strike_price': strike_price,
                'ask': ask,
                'ask_size': ask_size,
                'bid': bid,
                'bid_size': bid_size,
                'underlying_price': underlying_price,
                'distance': distance,
                'distance_percent': distance_percent
            }
            row = pd.DataFrame(row, index=[0])
            history = pd.concat([history, row], ignore_index=True)
        except:
            continue
        # else:
        #   print(ticker, 'Response 404', res)
    # print(tabulate(history, headers='keys', tablefmt='psql'))
    # print('\n', round(getsizeof(history)/1073741824,5), '\n')
    # history.to_csv('src/apis/db/callOptions.csv', index=False)
