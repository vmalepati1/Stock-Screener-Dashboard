import sys,os
sys.path.append(os.path.abspath(os.path.join('..')))

from financial_tests.financials_testing import get_financials_data
from app.home.finance.sectors import sectors

import csv

if __name__ == '__main__':
    fields = ['name', 'ticker', 'eps', 'pe', 'peg', 'ps', 'pb', 'valueToEbitda', 'debtToEbitda',
              'beta', 'grossMargin', 'operatingMargin', 'netMargin', 'dividendYield',
              'currentRatio', 'ROE', 'return1y', 'industryScore']

    sectors_list = [x['name'] for x in sectors]
    
    for sector in sectors_list:
        rows = [x.values() for x in get_financials_data(sector)]

        filename = "rankings/" + sector + ".csv"

        print('Writing to CSV')
        with open(filename, 'w', newline='') as csvfile:  
            csvwriter = csv.writer(csvfile)
                
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)

