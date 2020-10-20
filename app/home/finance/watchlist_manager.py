from flask_login import current_user
from app.home.finance.returns import get_optimal_interval
from app.home.finance.load_stock import load_stock

import concurrent.futures

def add_to_watchlist(current_watchlist, ticker):
    watchlist = current_watchlist

    watchlist = watchlist + ticker + ' '

    return watchlist

def remove_from_watchlist(current_watchlist, ticker):
    watchlist = current_watchlist

    watchlist = watchlist.replace(ticker + ' ', '')
    
    return watchlist

def get_watchlist_data(stocks, time_frame):
    CONNECTIONS = 100

    optimal_interval = get_optimal_interval(time_frame)
    
    stock_tickers = current_user.watchlist.split()

    stocks = [t for t in stocks if t['ticker'] in stock_tickers]

    watchlist_data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_stocks  = (executor.submit(load_stock, t['name'], t['ticker'], t['currency'], time_frame, optimal_interval) for t in stocks)

        for future in concurrent.futures.as_completed(future_to_stocks):
            try:
                data = future.result()

                if data:
                    watchlist_data.append(data)
            except Exception as exc:
                print(str(exc))
                print('Error loading data!')

    sorted_watchlist_data = sorted(watchlist_data, key=lambda k: k['change'], reverse=True)

    return sorted_watchlist_data
