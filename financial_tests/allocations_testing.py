import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime
import scipy.optimize as optimization
import yfinance as yf
import time
from multiprocessing import Pool

stocks = ['AMD', 'AAPL', 'MSEGX']

#we use historical data to approximate mean and variance: MPT depends on historical data !!!
start_date='2015-11-04'
end_date ='2020-11-04'

#downloading the data from Yahoo! Finance
def download_data(stocks):
	data = web.DataReader(stocks,data_source='yahoo',start=start_date,end=end_date)['Adj Close']
		
	return data
	
def show_data(data):
	data.plot(figsize=(10,5))
	plt.show()

#we usually use natural logarithm for normalization purposes
def calculate_returns(data):
	returns = np.log(data/data.shift(1))
	return returns;
	
def plot_daily_returns(returns):
	returns.plot(figsize=(10,5))
	plt.show()

#print out mean and covariance of stocks within [start_date, end_date]. There are 252 trading days within a year
def show_statistics(returns):
	print(returns.mean()*252)
	print(returns.cov()*252)

#weights defines what stocks to include (with what portion) in the portfolio
def initialize_weights(stocks):
	weights = np.random.random(len(stocks))
	weights /= np.sum(weights)
	return weights;
	
#expected portfolio return
def calculate_portfolio_return(returns, weights):
	portfolio_return = np.sum(returns.mean()*weights)*252
	print("Expected portfolio return:", portfolio_return)

#expected portfolio variance
def calculate_portfolio_variance(returns, weights):
	portfolio_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*252,weights)))
	print("Expected variance:", portfolio_variance)

def get_return_and_variance_c(i, returns, stocks_len):
	weights = np.random.random(stocks_len)
	weights/=np.sum(weights)
	return np.sum(returns.mean()*weights)*252, np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))

def get_return_and_variance_p(returns_and_stocks_len):
	returns = returns_and_stocks_len[0]
	stocks_len = returns_and_stocks_len[1]
	weights = np.random.random(stocks_len)
	weights/=np.sum(weights)
	return np.sum(returns.mean()*weights)*252, np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))

def generate_portfolios(weights, returns, stocks):
	CONNECTIONS = 100

##	preturns = []
##	pvariances = []

##	with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
##		future_to_data  = (executor.submit(get_return_and_variance_c, i, returns, len(stocks)) for i in range(10000))
##		
##		for future in concurrent.futures.as_completed(future_to_data):
##			try:
##				returns, variance = future.result()
##
##				preturns.append(returns)
##				pvariances.append(variance)
##			except Exception as exc:
##				print(str(exc))
##				print('Error calculating portfolio futures!')

	pool = Pool(5)

	returns_and_variances = pool.map(get_return_and_variance_p, [(returns, len(stocks))] * 10000)

	preturns, pvariances = zip(*returns_and_variances)

	#Monte-Carlo simulation: we generate several random weights -> so random portfolios !!!
##	for i in range(10000):
##		weights = np.random.random(len(stocks))
##		weights/=np.sum(weights)
##		preturns.append(np.sum(returns.mean()*weights)*252)
##		pvariances.append(np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights))))
	
	preturns = np.array(preturns)
	pvariances = np.array(pvariances)
	return preturns,pvariances

def plot_portfolios(returns, variances):
	plt.figure(figsize=(10,6))
	plt.scatter(variances,returns,c=returns/variances,marker='o')
	plt.grid(True)
	plt.xlabel('Expected Volatility')
	plt.ylabel('Expected Return')
	plt.colorbar(label='Sharpe Ratio')
	plt.show()

# OK this is the result of the simulation ... we have to find the optimal portfolio with 
# some optimization technique !!! scipy can optimize functions (minimum/maximum finding)
def statistics(weights, returns):
	portfolio_return=np.sum(returns.mean()*weights)*252
	portfolio_volatility=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
	return np.array([portfolio_return,portfolio_volatility,portfolio_return/portfolio_volatility])

# [2] means that we want to maximize according to the Sharpe-ration
# note: maximizing f(x) function is the same as minimizing -f(x) !!!
def min_func_sharpe(weights,returns):
	return	-statistics(weights,returns)[2] 
	
# what are the constraints? The sum of weights = 1 !!!  f(x)=0 this is the function to minimize
def optimize_portfolio(weights,returns, stocks):
	constraints = ({'type':'eq','fun': lambda x: np.sum(x)-1}) #the sum of weights is 1
	bounds = tuple((0,1) for x in range(len(stocks))) #the weights can be 1 at most: 1 when 100% of money is invested into a single stock
	optimum=optimization.minimize(fun=min_func_sharpe,x0=weights,args=returns,method='SLSQP',bounds=bounds,constraints=constraints) 
	return optimum
	
# optimal portfolio according to weights: 0 means no shares of that given company 
def get_optimal_portfolio(optimum, returns):
	return optimum['x'].round(3), statistics(optimum['x'].round(3),returns)

def show_optimal_portfolio(optimum, returns, preturns, pvariances):
	plt.figure(figsize=(10,6))
	plt.scatter(pvariances,preturns,c=preturns/pvariances,marker='o')
	plt.grid(True)
	plt.xlabel('Expected Volatility')
	plt.ylabel('Expected Return')
	plt.colorbar(label='Sharpe Ratio')
	plt.plot(statistics(optimum['x'],returns)[1],statistics(optimum['x'],returns)[0],'g*',markersize=20.0)
	plt.show()

def get_allocations_and_stats(stocks):
	data = download_data(stocks)
	#show_data(data)
	returns = calculate_returns(data)
	#plot_daily_returns(returns)
	# show_statistics(returns)
	weights=initialize_weights(stocks)
	# calculate_portfolio_return(returns,weights)
	# calculate_portfolio_variance(returns,weights)
	# preturns,pvariances=generate_portfolios(weights, returns, stocks)
	#plot_portfolios(preturns,pvariances)
	optimum=optimize_portfolio(weights,returns, stocks)
	return get_optimal_portfolio(optimum, returns)

weights, stats = get_allocations_and_stats(stocks)
print(stats)
print(weights)
