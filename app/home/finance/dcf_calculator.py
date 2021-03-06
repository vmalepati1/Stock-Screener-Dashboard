##from urllib.request import urlopen as Req
##from bs4 import BeautifulSoup as soup
##import yfinance as yf
##import numpy as np
##import pandas as pd
##
##from app.home.utils.beautify import beautify_financials
##
##def text_to_num(text):
##    d = {
##        'M': 6,
##        'B': 9
##    }
##
##    if text[-1] in d:
##        num, magnitude = text[:-1], text[-1]
##        return float(num) * 10 ** d[magnitude]
##    else:
##        return float(text)
##
##def get_projections(ticker_name):
##    url = 'https://finance.yahoo.com/quote/' + ticker_name + '/analysis?p=' + ticker_name
##
##    Client = Req(url)
##    # saves
##    page_hmtl = Client.read()
##    Client.close()
##
##    # parses the html of the website
##    page_soup = soup(page_hmtl, "html.parser")
##
##    value = page_soup.findAll("span",{"class":"Trsdu(0.3s)"})
##
##    currentVal = text_to_num(value[38].text)
##    nextVal = text_to_num(value[39].text)
##
##    return currentVal, nextVal
##
### TODO: Should scrape the ten year yield
##def get_fair_value(ticker_name, total_forecasted_periods=5, ten_year_yield=0.0095, perpetual_growth_rate=0.025):
##    stock = yf.Ticker(ticker_name)
##    income_statement = stock.financials.loc[:, ::-1]
##    balance_sheet = stock.balance_sheet.loc[:, ::-1]
##    cash_flows = stock.cashflow.loc[:, ::-1]
##
##    current_year_est, next_year_est = get_projections(ticker_name)
##
##    revenues = income_statement.loc['Total Revenue']
##    forecasted_revenues = pd.Series([current_year_est, next_year_est], index=['2020E', '2021E'])
##    all_revenues = pd.concat([revenues, forecasted_revenues])
##    revenue_growth_rate = all_revenues.pct_change().mean()
##
##    net_income_margins = income_statement.loc['Net Income'] / income_statement.loc['Total Revenue']
##    projected_net_income_margin = net_income_margins.median()
##
##    # FCF = CFO - CAPEX
##    free_cash_flows = cash_flows.loc['Total Cash From Operating Activities'] - cash_flows.loc['Capital Expenditures'].abs()
##    FCFE_to_NI = free_cash_flows / income_statement.loc['Net Income']
##    projected_FCFE_to_NI = FCFE_to_NI.median()
##    
##    total_debt = abs(balance_sheet.loc['Short Long Term Debt'].iloc[-1]) + abs(balance_sheet.loc['Long Term Debt'].iloc[-1])
##    rd = abs(income_statement.loc['Interest Expense'].iloc[-1]) / total_debt
##    
##    tax_rate = abs(income_statement.loc['Income Tax Expense'].iloc[-1]) / income_statement.loc['Income Before Tax'].iloc[-1]
##    cost_of_debt = rd * (1 - tax_rate)
##
##    beta = stock.info['beta']
##    cost_of_equity = ten_year_yield + beta * (0.098 - ten_year_yield)
##
##    market_cap = stock.info['marketCap']
##    total_financing = total_debt + market_cap
##
##    wacc = (total_debt / total_financing) * cost_of_debt + (market_cap / total_financing) * cost_of_equity
##    perpetual_growth = 0.025
##
##    revenues_for_forecasted_period = []
##
##    revenues_for_forecasted_period.append(current_year_est)
##    revenues_for_forecasted_period.append(next_year_est)
##    num_years_not_forecasted = total_forecasted_periods - 2
##
##    previous_year_forecast = next_year_est
##    
##    for i in range(0, num_years_not_forecasted):
##        new_forecast = previous_year_forecast * (1 + revenue_growth_rate)
##        revenues_for_forecasted_period.append(new_forecast)
##        previous_year_forecast = new_forecast
##
##    FCFs = []
##    discount_factors = []
##    present_values = []
##
##    for i, projected_revenue in enumerate(revenues_for_forecasted_period):
##        projected_net_income = projected_revenue * projected_net_income_margin
##        projected_FCF = projected_net_income * projected_FCFE_to_NI
##        discount_factor = pow(1 + wacc, i + 1)
##        PV_FCF = projected_FCF / discount_factor
##
##        FCFs.append(projected_FCF)
##        discount_factors.append(discount_factor)
##        present_values.append(PV_FCF)
##
##    TV = (present_values[-1] * (1 + perpetual_growth)) / (wacc - perpetual_growth)
##    last_discount_factor = pow(1 + wacc, total_forecasted_periods)
##    PV_of_TV = TV / last_discount_factor
##
##    FCFs.append(TV)
##    FCFs = [free_cash_flows[-1]] + FCFs
##    discount_factors.append(last_discount_factor)
##    present_values.append(PV_of_TV)
##
##    value_today = sum(present_values)
##    shares_outstanding = stock.info['sharesOutstanding']
##    fair_value = value_today / shares_outstanding
##
##    historical_data = stock.history(period = '1d', interval = '1h')
##    current_trading_price = historical_data['Close'].iloc[-1]
##
##    upside = (fair_value - current_trading_price) / current_trading_price
##
##    revenues_row = revenues.iloc[-2:].tolist() + revenues_for_forecasted_period
##    revenue_growth_row = np.diff(revenues_row) / revenues_row[:-1]
##    revenues_row.pop(0)
##
##    metrics = [revenue_growth_rate, cost_of_debt, cost_of_equity, wacc, perpetual_growth_rate]
##
##    return metrics, beautify_financials(revenues_row), revenue_growth_row, beautify_financials(FCFs), \
##           discount_factors, beautify_financials(present_values), fair_value, current_trading_price, upside
##

import xlrd

wb = xlrd.open_workbook('data/dcf_data.xls')
sheet = wb.sheet_by_index(0)

def get_dcf_data(ticker_name):
    start_idx = -1

    for row_num in range(sheet.nrows):
        row_value = sheet.row_values(row_num)
        if row_value[0] == ticker_name:
            start_idx = row_num
            break

    if start_idx == -1:
        return False, None, None, None, None

    first_row = sheet.row_values(start_idx)

    fair_value = '{:.2f}'.format(first_row[1])
    current_price = '{:.2f}'.format(first_row[2])
    upside = first_row[3] / 100.0

    FCFs = []
    revenues_row = []
    revenue_growth_row = []

    for i in range(start_idx, start_idx + 5):
        row_value = sheet.row_values(i)
        
        FCF_unformatted = row_value[6]
        revenue_unformatted = row_value[7]
        revenue_growth_unformatted = row_value[8]

        FCF = '{:,.0f}'.format(FCF_unformatted)
        revenue = '{:,.0f}'.format(revenue_unformatted)
        revenue_growth = '{0}%'.format(revenue_growth_unformatted)

        FCFs.append(FCF)
        revenues_row.append(revenue)
        revenue_growth_row.append(revenue_growth)

    calculation_values = []

    count = 0

    for i in range(start_idx+5, start_idx+11):
        row_value = sheet.row_values(i)[6]
        
        if count == 1 or count == 3:
            calculations_value = '{0}%'.format(row_value)
        else:
            calculations_value = '{:,.0f}'.format(row_value)

        calculation_values.append(calculations_value)
        
        count += 1

    return True, fair_value, current_price, upside, FCFs, revenues_row, revenue_growth_row, calculation_values
