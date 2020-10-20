import sys,os
sys.path.append(os.path.abspath(os.path.join('..')))

from app.home.finance.stocks_dict import stocks_dict

import yfinance as yf
import concurrent.futures
import pprint

def load_sector_stock(ticker_name):
    ticker = yf.Ticker(ticker_name)

    try:
        company_name = ticker.info['shortName']
    except:
        company_name = 'Error'

    try:
        currency = ticker.info['currency']
    except:
        currency = 'USD'

    return {
            'name': company_name,
            'ticker': ticker_name,
            'currency': currency
        }

CONNECTIONS = 100

detailed_dict = {
    'Consumer Discretionary': None,
    'Consumer Staples': None,
    'Energy': None,
    'Financial Services': None,
    'Healthcare': None,
    'Materials & Processing': None,
    'Producer Durables': None,
    'Technology': None,
    'Utilities': None,
}

for sector in detailed_dict:
    d = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_stocks  = (executor.submit(load_sector_stock, t) for t in stocks_dict[sector])

        for future in concurrent.futures.as_completed(future_to_stocks):
            try:
                data = future.result()
                d.append(data)
            except Exception as exc:
                print('Error loading data!')

    detailed_dict[sector] = d

with open('output/detailed_dict.txt','w') as fout:
    pprint.pprint(detailed_dict,stream=fout)
    
