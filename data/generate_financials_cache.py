import sys,os
sys.path.append(os.path.abspath(os.path.join('..')))

import concurrent.futures
import yfinance as yf
import pandas as pd
import csv

from app.home.finance.stocks_dict import stocks_dict

def load_cache_data(ticker_name):
    ticker = yf.Ticker(ticker_name)
    
    info = ticker.info

    if 'trailingEps' in info:
        eps = info['trailingEps']
    else:
        eps = info['forwardEps']
    
    if 'trailingPE' in info:
        pe = info['trailingPE']
    else:
        pe = info['forwardPE']

    peg = info['pegRatio']
    ps = info['priceToSalesTrailing12Months']
    pb = info['priceToBook']
    valueToEbitda = info['enterpriseToEbitda']
    dividendYield = info['dividendYield']
    beta = info['beta']
    bookValue = info['bookValue'] * info['sharesOutstanding']
    industry = info['industry']

    return [ticker_name, eps, pe, peg, ps, pb, valueToEbitda, dividendYield, beta, bookValue, industry]

if __name__ == '__main__':
    fields = ['Ticker', 'EPS', 'PE', 'PEG', 'PS', 'PB', 'VEBITDA', 'Dividend Yield', 'Beta', 'Book Value', 'Industry']
    
    CONNECTIONS = 100

    rows = []

    all_stocks_unordered = sum(stocks_dict.values(), [])
    all_stocks = sorted(all_stocks_unordered, key = lambda s: s['ticker'])
    all_stocks = all_stocks[400:491]

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_financials  = (executor.submit(load_cache_data, t['ticker']) for t in all_stocks)

        for future in concurrent.futures.as_completed(future_to_financials):
            try:
                data = future.result()

                rows.append(data)
            except Exception as exc:
                print(str(exc))
                print('Error loading financials!')

    filename = "financials-cache.csv"

    print('Writing to CSV')
    with open(filename, 'w', newline='') as csvfile:  
        csvwriter = csv.writer(csvfile)
            
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
