import sys,os
sys.path.append(os.path.abspath(os.path.join('..')))

from app.home.finance.stocks_dict import stocks_dict

import yfinance as yf

# checks to see that tickers are valid and prints those that are not

for sector in stocks_dict:
    print('Checking {} sector'.format(sector))
    
    for stock in stocks_dict[sector]:
        try:
            ticker_name = stock['ticker']
            ticker = yf.Ticker(ticker_name)
        except:
            continue

        ticker_historical = ticker.history(period="1y", interval="3mo")

        if ticker_historical.empty:
            print('{} does not work'.format(ticker_name))
