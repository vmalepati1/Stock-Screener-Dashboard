import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

def get_forecast_data(ticker_name):
    # Get the stock data (a library that essentially pulls financial data for you)
    ticker = yf.Ticker(ticker_name)

    df = ticker.history(  # or pdr.get_data_yahoo(...
        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = '2y',

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = '1d',
    )
    # Shows the initial data pulled from quandl

    # Get the Adjusted Close Price
    df = df[['Close']]
    # Show the new data based off of the adjustments

    # A variable for predicting 'n' days out into the future
    # n=50 days
    forecast = 15
    # Create another column (the target) shifted 'n' units up
    # shifts due to the forecast
    df['Prediction'] = df[['Close']].shift(-forecast)
    # prints the new data set after the new column

    ### Create a new independent data set for the X values
    # Use the numpy library to convert parts of the database to an array
    X = np.array(df.drop(['Prediction'], 1))

    # Remove the last '50' rows
    X = X[:-forecast]

    ### Create the dependent data set (Y)  #####
    # Convert the dataframe to a numpy array
    Y = np.array(df['Prediction'])
    # Get all of the y values except the last '30' rows
    Y = Y[:-forecast]
    
    # Split all of the data being created into 20% testing and the rest for training the model
    # x_train and y_train is training the x and y vals to fit to the model
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, train_size=0.8)

    # Create and train the Support Vector Machine (Regressor)
    # Write
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_rbf.fit(x_train, y_train)

    # testing model that is from the internet and returns the R^2 value of the model
    # a higher score shows a closer fit and the best possible number is 1
    svm_confidence = svr_rbf.score(x_test, y_test)
    # creating the initial model
    linReg = LinearRegression()
    # training the models (80% of the model)
    linReg.fit(x_train, y_train)

    # testing model that is from the internet and returns the R^2 value of the model
    # essentially a goodness_of_fit test in a number, highest number is a 1, same as above
    # linear regression confidence (read up on the internet for more information)
    linReg_confidence = linReg.score(x_test, y_test)

    # set x_forecast equal to the last x rows of the original data set from Adj. Close column
    x_forecast = np.array(df.drop(['Prediction'], 1))[-forecast:]
    # print linear regression model predictions for the next x days
    linReg_prediction = linReg.predict(x_forecast)
    
    # Print support vector regressor model predictions for the next x days
    svm_prediction = svr_rbf.predict(x_forecast)

    return linReg_prediction, svm_prediction
