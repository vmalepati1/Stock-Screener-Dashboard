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

    n_symbols = 30

    tickers_start_idx = 14
    names_start_idx = 0
    price_start_idx = 0
    changes_start_idx = 2
    volume_start_idx = 0
    avg_volume_start_idx = 0

    tickers_html = page_soup.findAll("a", {"class":"Fw(b)"})
    prices_html = page_soup.findAll("td", {"class": "data-col2 Ta(end) Pstart(10px) Pend(6px) Fw(b)"})
    changes_html = page_soup.findAll("td", {"class": "data-col4 Ta(end) Pstart(10px) Pend(6px)"})
    volumes_html = page_soup.findAll("td", {"class": "data-col6 Ta(end) Pstart(10px) Pend(6px)"})
    avg_volumes_html = page_soup.findAll("td", {"class": "data-col7 Ta(end) Pstart(10px) Pend(6px)"})

    data = []

    for i in range(n_symbols):
        ticker = tickers_html[tickers_start_idx + i]["title"]
        price = prices_html[price_start_idx + i].text
        change = changes_html[changes_start_idx + i].text
        volume = volumes_html[volume_start_idx + i].text
        avg_volume = avg_volumes_html[avg_volume_start_idx + i].text

        data.append((ticker, price, change, volume, avg_volume))

    return data

def getMostOwnedData():
    most_owned_df = pd.read_excel('../data/most-owned-data-10-18-20.xlsx')

    return most_owned_df['Symbol'].tolist()
        
print(getMostBoughtData())

