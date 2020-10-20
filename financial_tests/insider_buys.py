import requests
from bs4 import BeautifulSoup as soup

def getInsiderBuyData():
    my_url = 'https://finviz.com/insidertrading.ashx?tc=1'

    # saves the information from the url into the client
    resp = requests.get(my_url)

    print(resp.text)

    # parses the html of the website
    page_soup = soup(resp.text, "html.parser")

    tickers_html = page_soup.findAll("a", {"class":"tab-link"})

    print(tickers_html)

getInsiderBuyData()
