import concurrent.futures
import yfinance as yf
import pandas as pd
import math

import sys,os
sys.path.append(os.path.abspath(os.path.join('..')))

from app.home.finance.stocks_dict import stocks_dict
from app.home.finance.industry_lut import industry_lut

def calculate_score_lower(stat, industry_avg):
    return (industry_avg - stat) / industry_avg

def calculate_score_higher(stat, industry_avg):
    return (stat - industry_avg) / industry_avg

def beautify_ratio(ratio):
    if ratio is not None:
        return str(round(ratio, 2))
    else:
        return 'NA'

def beautify_percentage(percentage):
    if percentage is not None:
        return str(round(100*percentage, 2))
    else:
        return 'NA'

def load_financials(company_name, ticker_name, 
                    pe_industry, ps_industry, pbv_industry,
                    vebtida_industry, beta_industry, margin_industry):
    
    ticker = yf.Ticker(ticker_name)
    info = ticker.info
    financials = ticker.financials
    balance_sheet = ticker.balance_sheet
    cash_flow = ticker.cashflow

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

    TR = financials.iloc[:, 0].loc['Total Revenue']
    COGS = financials.iloc[:, 0].loc['Cost Of Revenue']
    
    grossMargin = (TR - COGS) / TR

    operatingIncome = financials.iloc[:, 0].loc['Operating Income']

    operatingMargin = operatingIncome / TR

    netIncome = financials.iloc[:, 0].loc['Net Income']

    netMargin = netIncome / TR

    beta = info['beta']

    bookValue = info['bookValue'] * info['sharesOutstanding']

    ROE = netIncome / bookValue

    # Rough estimate; ignores amortization
    debtToEbitda = (balance_sheet.iloc[:, 0].loc['Total Liab']) \
                        / (financials.iloc[:, 0].loc['Ebit'] + cash_flow.iloc[:, 0].loc['Depreciation'])

    currentRatio = balance_sheet.iloc[:, 0].loc['Total Current Assets'] / balance_sheet.iloc[:, 0].loc['Total Current Liabilities']

    industry = info['industry']
    spreadsheet_industry = industry_lut[industry]
    
    pe_i = pe_industry.loc[spreadsheet_industry, 'Current PE'].item()
    peg_i = pe_industry.loc[spreadsheet_industry, 'PEG Ratio'].item()
    ps_i = ps_industry.loc[spreadsheet_industry, 'Price/Sales'].item()
    pb_i = pbv_industry.loc[spreadsheet_industry, 'PBV'].item()
    v_ebitda_i = vebtida_industry.loc[spreadsheet_industry, 'EV/EBITDA3'].item()
    beta_i = beta_industry.loc[spreadsheet_industry, 'Beta '].item()

    gross_margin_i = margin_industry.loc[spreadsheet_industry, 'Gross Margin'].item()
    operating_margin_i = ps_industry.loc[spreadsheet_industry, 'Pre-tax Operating Margin'].item()
    net_margin_i = margin_industry.loc[spreadsheet_industry, 'Net Margin'].item()

    ROE_i = pbv_industry.loc[spreadsheet_industry, 'ROE'].item()

    ticker_historical = ticker.history(  # or pdr.get_data_yahoo(...
        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = '1y',

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = '3mo',
    )

    start_price = ticker_historical['Open'].iloc[0]
    end_price = ticker_historical['Close'].iloc[-1]

    i = 1
    
    while math.isnan(start_price):
        start_price = ticker_historical['Open'].iloc[i]
        
        i += 1

    i = -2
    
    while math.isnan(end_price):
        end_price = ticker_historical['Close'].iloc[i]
        
        i -= 1
    
    change = (end_price - start_price) / start_price

    # weighted average of how the stock performs relative to industry
    # more emphasis on ROE and margins, less on valuation ratios

##    if not pe:
##        pe = pe_i
##    if not peg:
##        peg = peg_i
##    if not ps:
##        ps = ps_i
##    if not pb:
##        pb = pb_i
##    if not valueToEbitda:
##        valueToEbitda = v_ebitda_i
##    if not beta:
##        beta = beta_i
##    if not grossMargin:
##        grossMargin = gross_margin_i
##    if not operatingMargin:
##        operatingMargin = operating_margin_i
##    if not netMargin:
##        netMargin = net_margin_i
##    if not ROE:
##        ROE = ROE_i

    if pe < 0 or peg < 0 or ps < 0 or pb < 0 or valueToEbitda < 0 or beta < 0 or netMargin < 0 or ROE < 0:
        industry_score = 'NA'
    else:
        industry_score = 0.075*calculate_score_lower(pe, pe_i) + 0.025*calculate_score_lower(peg, peg_i) + \
                        0.075*calculate_score_lower(ps, ps_i) + 0.05*calculate_score_lower(pb, pb_i) + \
                        0.05*calculate_score_lower(valueToEbitda, v_ebitda_i) + 0.025*calculate_score_lower(beta, beta_i) + \
                        0.175*calculate_score_higher(grossMargin, gross_margin_i) + 0.175*calculate_score_higher(operatingMargin, operating_margin_i) + \
                        0.175*calculate_score_higher(netMargin, net_margin_i) + 0.175*calculate_score_higher(ROE, ROE_i)

        print(industry_score)
##        if math.isnan(industry_score):
##            industry_score = 'NA'
##        else:
        industry_score = beautify_ratio(industry_score)

    return {
            'name': company_name,
            'ticker': ticker_name,
            'eps': beautify_ratio(eps),
            'pe': beautify_ratio(pe),
            'peg': beautify_ratio(peg),
            'ps': beautify_ratio(ps),
            'pb': beautify_ratio(pb),
            'valueToEbitda': beautify_ratio(valueToEbitda),
            'debtToEbitda': beautify_ratio(debtToEbitda),
            'beta': beautify_ratio(beta),
            'grossMargin': beautify_percentage(grossMargin),
            'operatingMargin': beautify_percentage(operatingMargin),
            'netMargin': beautify_percentage(netMargin),
            'dividendYield': beautify_percentage(dividendYield),
            'currentRatio': beautify_ratio(currentRatio),
            'ROE': beautify_percentage(ROE),
            'return1y': beautify_percentage(change),
            'industryScore': industry_score
        }

pe_industry = pd.read_excel('../data/pedata.xls', skiprows=7, index_col=0)
ps_industry = pd.read_excel('../data/psdata.xls', skiprows=7, index_col=0)
pbv_industry = pd.read_excel('../data/pbvdata.xls', skiprows=7, index_col=0)
vebtida_industry = pd.read_excel('../data/vebitda.xls', skiprows=8, index_col=0)
beta_industry = pd.read_excel('../data/betas.xls', skiprows=9, index_col=0, sheet_name='Industry Averages')
margin_industry = pd.read_excel('../data/margin.xls', skiprows=8, index_col=0)

print('hello')
# load_financials('Wendys', 'WEN', pe_industry, ps_industry, pbv_industry, vebtida_industry, beta_industry, margin_industry)
