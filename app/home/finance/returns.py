from app.home.finance.time_frames import time_frames
import yfinance as yf

def get_optimal_interval(time_frame):
    if time_frame in [t['name'] for t in time_frames]:
        if time_frame == '1d':
            return '90m'
        elif time_frame == '5d':
            return '1d'
        elif time_frame == '1mo':
            return '1wk'
        elif time_frame == '3mo':
            return '1mo'
        else:
            return '3mo'
    else:
        return '1d'

def get_price_and_return(ticker_name, time_frame):
    ticker = yf.Ticker(ticker_name)

    ticker_historical = ticker.history(period=time_frame, interval=get_optimal_interval(time_frame))

    start_price = ticker_historical['Open'].iloc[0]
    end_price = ticker_historical['Close'].iloc[-1]
    
    return end_price, (end_price - start_price) / start_price
