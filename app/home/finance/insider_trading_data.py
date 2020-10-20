from urllib.request import urlopen as Req
from bs4 import BeautifulSoup as soup

def get_insider_trading_data():
    my_url = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1'

    Client = Req(my_url)

    page_html = Client.read()
    Client.close()

    page_soup = soup(page_html, "html.parser")

    # finds the ticker locations using this method
    findsT = page_soup.findAll("a",{"onmouseout":"UnTip()"})

    # finds the title of the person that was insider trading
    findsTi = page_soup.findAll("td")

    # finds the title of the person trading on the inside
    findsNum = page_soup.findAll("td",{"align":"right"})

    x = 0 # variable for the title
    y = 22 # finds the price of the stock when bought
    z = 23 # finds the quantity of stocks purchased
    w = 24 # finds the number of stocks already owned
    a = 72 # finds the title of the person insider trading

    data = []
    
    while x < 1000:
        findT = findsT[x]
        findT = findT["href"].replace("/", "")
        findP = findsNum[y].text
        findQ = findsNum[z].text
        findO = findsNum[w].text
        findTi = findsTi[a].text
        data.append((findT, findTi, findP, findQ, findO))
        x += 1
        y += 12
        z += 12
        w += 12
        a += 17

    return data
