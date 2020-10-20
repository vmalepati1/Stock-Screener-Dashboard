import sys,os
sys.path.append(os.path.abspath(os.path.join('..')))

from app.home.finance.top_gainers import get_top_gainers
import yfinance as yf

gainers = get_top_gainers('Technology', '5d')

print(gainers)
