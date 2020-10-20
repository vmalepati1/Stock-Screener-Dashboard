import sys,os
sys.path.append(os.path.abspath(os.path.join('..')))

from app.home.finance.stocks_dict import stocks_dict

import yfinance as yf
import pprint

# creates a dict containing the industry names on Yahoo Finance

industries = set()

for sector in stocks_dict:
    print('Checking {} sector'.format(sector))
    
    for stock in stocks_dict[sector]:
        try:
            ticker_name = stock['ticker']
            ticker = yf.Ticker(ticker_name)

            industry = ticker.info['industry']
            print(industry)

            industries.add(industry)
        except:
            continue

industries_dict = dict.fromkeys(industries, '')

with open('output/industries_lut.txt','w') as fout:
    pprint.pprint(industries_dict,stream=fout)
