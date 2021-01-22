from urllib.request import urlopen as Req
from bs4 import BeautifulSoup as soup
import pandas as pd

# do the class a with the class and the fw(b) in order to get all the titles
# loops through the different ticker classes in order to grab all the titles
# also gets percent changes
def getMostBoughtData():
    my_url = 'https://finance.yahoo.com/u/yahoo-finance/watchlists/most-bought-by-hedge-funds/'

    # saves the information from the url into the client
    Client = Req(my_url)

    # saves
    page_hmtl = Client.read()
    Client.close()

    # parses the html of the website
    page_soup = soup(page_hmtl, "html.parser")

    # finds all the parts of the webpage that would hold the titles
    symbols = page_soup.findAll("h2",{"class":"Fz(m)"})
    tickers = page_soup.findAll("a", {"class":"Fw(b)"})
    prices_html = page_soup.findAll("td", {"class": "data-col2 Ta(end) Pstart(10px) Pend(6px) Fw(b)"})
    changes_html = page_soup.findAll("td", {"class": "data-col4 Ta(end) Pstart(10px) Pend(6px)"})
    volumes_html = page_soup.findAll("td", {"class": "data-col6 Ta(end) Pstart(10px) Pend(6px)"})
    avg_volumes_html = page_soup.findAll("td", {"class": "data-col7 Ta(end) Pstart(10px) Pend(6px)"})

    sym = int(symbols[1].text[0:2])

    x = 0

    data = []
    
    while x < 48-1:
        if len(tickers[x].text) > 5 or tickers[x].text == "Tech" or tickers[x].text == "News":
            x = x + 1
        else:
            break
    y = x
    while x < y + sym:
        ticker = tickers[x].text
        price = prices_html[x - (y + sym)].text
        
        change_str = changes_html[x - (y + sym)].text

        if change_str.startswith('+'):
            change = change_str[1:]
        else:
            change = change_str
        
        volume = volumes_html[x - (y + sym)].text
        avg_volume = avg_volumes_html[x - (y + sym)].text

        data.append((ticker, price, change, volume, avg_volume))
        
        x = x + 1

    return data

def getMostOwnedData():
    most_owned_df = pd.read_excel('data/most-owned-data-10-18-20.xlsx', engine='openpyxl')

    return most_owned_df['Symbol'].tolist()
