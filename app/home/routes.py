# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app import db
from app.home import blueprint
from app.home.forms import EditProfileForm
from app.home.finance.sectors import sectors, SPDR_ETFs
from app.home.finance.time_frames import time_frames
from app.home.finance.top_gainers import get_top_gainers
from app.home.finance.time_frames import time_frames
from app.home.finance.returns import get_price_and_return
from app.home.finance.stocks_dict import stocks_dict
from app.home.finance.watchlist_manager import *
from app.home.finance.allocations import get_allocations_and_stats
from app.home.finance.insider_trading_data import get_insider_trading_data
from app.home.finance.hedge_fund_data import *
from app.home.finance.financials_data import get_financials_data
from app.home.finance.dcf_calculator import get_fair_value
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import math

@blueprint.route('/index')
@login_required
def index():
    return redirect(url_for('home_blueprint.edit_profile'))

@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_form = EditProfileForm(request.form)
    
    if 'save' in request.form:
        if edit_form.validate():
            current_user.username = request.form['username']
            current_user.email = request.form['email']
            current_user.first_name = request.form['first_name']
            current_user.last_name = request.form['last_name']
            current_user.sector = request.form['sector']

            db.session.commit()
        
            return render_template('profile.html', segment='profile', success='Changes successfully saved!', form=edit_form, sector_select_data=sectors)
        else:
            return render_template('profile.html', segment='profile', msg='Failed to save changes! Please check below.', form=edit_form, sector_select_data=sectors)
    else:
        return render_template('profile.html', segment='profile', form=edit_form, sector_select_data=sectors)

@blueprint.route('/top_gainers/<string:sector>/<string:time_frame>',  methods=['GET', 'POST'])
@login_required
def top_gainers(sector, time_frame):
    if sector not in [s['name'] for s in sectors] \
       or time_frame not in [tf['name'] for tf in time_frames]:
        return render_template('page-404.html'), 404
    
    SPDR_ETF = SPDR_ETFs[sector]
    price, change = get_price_and_return(SPDR_ETF, time_frame)
    gainers = get_top_gainers(sector, time_frame)

    if 'add' in request.form:
        current_user.watchlist = add_to_watchlist(current_user.watchlist, request.form['add'])
        
        db.session.commit()
    elif 'remove' in request.form:
        current_user.watchlist = remove_from_watchlist(current_user.watchlist, request.form['remove'])

        db.session.commit()
    
    return render_template('top_gainers.html', segment='gainers', sector_select_data=sectors, time_frame_select_data=time_frames, sector=sector,
                                   time_frame=time_frame, SPDR_ETF=SPDR_ETF, SPDR_price=price, SPDR_change=change, gainers=gainers)

@blueprint.route('/watchlist/<string:time_frame>',  methods=['GET', 'POST'])
@login_required
def watchlist(time_frame):
    stocks = sum(stocks_dict.values(), [])
    stocks = sorted(stocks, key = lambda i: i['ticker'])

    if time_frame not in [tf['name'] for tf in time_frames]:
        return render_template('page-404.html'), 404

    if 'add' in request.form:
        current_user.watchlist = add_to_watchlist(current_user.watchlist, request.form['symbol'])

        db.session.commit()
    elif 'remove' in request.form:
        current_user.watchlist = remove_from_watchlist(current_user.watchlist, request.form['remove'])

        db.session.commit()

    watchlist_stocks = get_watchlist_data(stocks, time_frame)
    
    return render_template('watchlist.html', segment='watchlist', time_frame_select_data=time_frames, stocks_list=stocks, time_frame=time_frame,
                           watchlist_stocks=watchlist_stocks)

@blueprint.route('/allocations')
@login_required
def allocations():
    stock_tickers = current_user.watchlist.split()
    allocations_data = None
    stats = None

    if len(stock_tickers) >= 1:
        weights, stats = get_allocations_and_stats(stock_tickers)

        allocations_data = {
            'datasets': [
                    {'data': [round(w * 100, 2) for w in weights]}
                ],

            'labels': current_user.watchlist.split()
        }

    return render_template('allocations.html', segment='allocations', allocations_data=allocations_data, stats=stats)

@blueprint.route('/hedge_funds/<string:sector>',  methods=['GET', 'POST'])
@login_required
def hedge_funds(sector):
    if sector not in [s['name'] for s in sectors]:
        return render_template('page-404.html'), 404
    
    most_bought_data = getMostBoughtData()
    most_bought_tickers = [x[0] for x in most_bought_data]

    most_owned_tickers = getMostOwnedData()
    
    most_bought_rows = []
    most_owned_rows = []

    if 'add' in request.form:
        current_user.watchlist = add_to_watchlist(current_user.watchlist, request.form['add'])

        db.session.commit()
    elif 'remove' in request.form:
        current_user.watchlist = remove_from_watchlist(current_user.watchlist, request.form['remove'])

        db.session.commit()

    for stock in stocks_dict[sector]:
        if stock['ticker'] in most_bought_tickers:
            idx = most_bought_tickers.index(stock['ticker'])
            data = most_bought_data[idx]

            most_bought_rows.append({
                    'ticker': data[0],
                    'name': stock['name'],
                    'price': data[1],
                    'currency': stock['currency'],
                    'change': data[2],
                    'volume': data[3],
                    'avg_volume': data[4]
                })

        if stock['ticker'] in most_owned_tickers:
            most_owned_rows.append({
                    'ticker': stock['ticker'],
                    'name': stock['name'],
                })

    return render_template('hedge_funds.html', segment='hedge', sector_select_data=sectors, sector=sector, most_bought_rows=most_bought_rows,
                           most_owned_rows=most_owned_rows)

@blueprint.route('/insider_trading/<string:sector>',  methods=['GET', 'POST'])
@login_required
def insider_trading(sector):
    if sector not in [s['name'] for s in sectors]:
        return render_template('page-404.html'), 404
    
    sector_tickers = [s['ticker'] for s in stocks_dict[sector]]
    insider_trading_data = get_insider_trading_data()
    
    insider_trade_rows = []

    if 'add' in request.form:
        current_user.watchlist = add_to_watchlist(current_user.watchlist, request.form['add'])

        db.session.commit()
    elif 'remove' in request.form:
        current_user.watchlist = remove_from_watchlist(current_user.watchlist, request.form['remove'])

        db.session.commit()

    for insider_trade in insider_trading_data:
        ticker = insider_trade[0]
        title = insider_trade[1]
        price = insider_trade[2]
        quantity = insider_trade[3]
        owned = insider_trade[4]

        stock = next((s for s in stocks_dict[sector] if s["ticker"] == ticker), None)

        if stock:
            insider_trade_rows.append({
                    'ticker': ticker,
                    'name': stock['name'],
                    'title': title,
                    'price': price,
                    'currency': stock['currency'],
                    'quantity_bought': quantity,
                    'shares_owned': owned
                })

    return render_template('insider_trading.html', segment='insider', sector_select_data=sectors, sector=sector, insider_trade_rows=insider_trade_rows)

@blueprint.route('/financials/<string:sector>',  methods=['GET', 'POST'])
@login_required
def financials(sector):
    if sector not in [s['name'] for s in sectors]:
        return render_template('page-404.html'), 404
    
    financials_rows = get_financials_data(sector)

    if 'add' in request.form:
        current_user.watchlist = add_to_watchlist(current_user.watchlist, request.form['add'])

        db.session.commit()
    elif 'remove' in request.form:
        current_user.watchlist = remove_from_watchlist(current_user.watchlist, request.form['remove'])

        db.session.commit()

    return render_template('financials.html', segment='financials', sector_select_data=sectors, sector=sector, financials_rows=financials_rows)

@blueprint.route('/dcf', defaults={'ticker': None})
@blueprint.route('/dcf/<string:ticker>',  methods=['GET'])
@login_required
def dcf(ticker):
    stocks = sum(stocks_dict.values(), [])
    stocks = sorted(stocks, key = lambda i: i['ticker'])

    if ticker:
        try:
            stock_info = next(s for s in stocks if s['ticker'] == ticker)
            currency = stock_info['currency']
        
            revenue_growth_rate, cost_of_debt, cost_of_equity, wacc, perpetual_growth_rate, \
                   revenues_row, revenue_growth_row, FCFs, discount_factors, present_values, \
                   fair_value, current_trading_price, upside = get_fair_value(ticker)

            if fair_value <= 0 or math.isnan(fair_value):
                return render_template('dcf.html', segment='dcf', stocks_list=stocks, ticker=ticker, msg='Unfortunately, there are insufficient analyst projections to develop a DCF model for this stock. Please select another symbol.')

            print(ticker)

            return render_template('dcf.html', segment='dcf', stocks_list=stocks, ticker=ticker, current_price=current_trading_price, currency=currency, fair_value=fair_value, upside=upside)
        except:
            return render_template('dcf.html', segment='dcf', stocks_list=stocks, ticker=ticker, msg='Unfortunately, there are insufficient analyst projections to develop a DCF model for this stock. Please select another symbol.')
    else:
        return render_template('dcf.html', segment='dcf', stocks_list=stocks, ticker=ticker)

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as exc:
        print(str(exc))
        return render_template('page-500.html'), 500
    

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
