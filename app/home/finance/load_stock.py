import yfinance as yf
import math

# Slow but supports all tickers
def load_stock(company_name, ticker_name, currency, time_frame, interval):
    # ticker = yf.Ticker(ticker_name)

    try:
        ticker = yf.Ticker(ticker_name)
    except:
        return None

    ticker_historical = ticker.history(  # or pdr.get_data_yahoo(...
        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = time_frame,

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = interval,
    )
    
    if ticker_historical.empty:
        return None

    start_price = ticker_historical['Open'].iloc[0]
    end_price = ticker_historical['Close'].iloc[-1]

    i = 1
    
    while math.isnan(start_price):
        start_price = ticker_historical['Open'].iloc[i]
        
        i += 1

    i = -2
    
    while math.isnan(end_price):
        end_price = ticker_historical['Close'].iloc[i]
        
        i -= 1
    
    change = (end_price - start_price) / start_price

    stock = {
        'company': company_name,
        'ticker': ticker_name,
        'last_price': end_price,
        'change': change,
        'currency': currency
    }

    return stock

### Fast but has trouble with a few tickers
##def load_stock_fast(ticker_name, time_frame, interval):
##    # ticker = yf.Ticker(ticker_name)
##
##    try:
##        ticker = yf.Ticker(ticker_name)
##    except:
##        return None
##
##    ticker_historical = yf.download(  # or pdr.get_data_yahoo(...
##        # tickers list or string as well
##        tickers = ticker_name,
##
##        # use "period" instead of start/end
##        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
##        # (optional, default is '1mo')
##        period = time_frame,
##
##        # fetch data by interval (including intraday if period < 60 days)
##        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
##        # (optional, default is '1d')
##        interval = interval,
##
##        # group by ticker (to access via data['SPY'])
##        # (optional, default is 'column')
##        group_by = 'ticker',
##
##        # adjust all OHLC automatically
##        # (optional, default is False)
##        auto_adjust = False,
##
##        # download pre/post regular market hours data
##        # (optional, default is False)
##        prepost = False,
##
##        # use threads for mass downloading? (True/False/Integer)
##        # (optional, default is True)
##        threads = False,
##
##        # proxy URL scheme use use when downloading?
##        # (optional, default is None)
##        proxy = None
##    )
##    
##    if ticker_historical.empty:
##        return None
##
##    start_price = ticker_historical['Open'].iloc[0]
##    end_price = ticker_historical['Close'].iloc[-1]
##    
##    change = (end_price - start_price) / start_price
##
####    company_name = ticker.info['shortName']
####    currency = ticker.info['currency']
##    
####    try:
####        
####    except:
####        company_name = 'Error'
####
####    try:
####        sma = ticker.info['fiftyDayAverage']
####    except:
####        sma = start_price
####
####    try:
####        currency = ticker.info['currency']
####    except:
####        currency = 'USD'
##
##    stock = {
##        'name': 'lol',
##        'ticker': ticker_name,
##        'last_price': end_price,
##        'currency': 'USD',
##        'change': change,
##    }
##
##    return stock
