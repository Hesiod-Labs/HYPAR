import scipy
import numpy as np
from scipy import exp, stats, log, sqrt
from scipy.stats import norm
import pandas as pd
import pandas_datareader.data as pdr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
# package imports
from broker import *
from exceptions import InvalidModelError


# Brownian motion is a simple continuous stochastic process that is widely used in physics
# and finance for modeling random behavior that evolves over time.
# Examples of such behavior are the random movements of a molecule of gas
# or fluctuations in an asset's price.
def brownian_motion(dt=0.1, N=1000):
    W = scipy.zeros(N+1)
    t = scipy.linspace(0, N, N+1)
    W[1:N+1] = scipy.cumsum(scipy.random.normal(0,dt,N))
    return t, W


# play is call or put
def blackscholes_model(stock_price, strike_price, expiration, risk_free_rate, sigma, play):
    # example parameters: stock_price = 100, strike_price = 100, expiration = 1 aka 1 year, rfr = 0.05, sigma = 2
    d1 = (log(stock_price/strike_price)+(risk_free_rate+sigma*sigma/2.0)*expiration)/(sigma*sqrt(expiration))
    d2 = d1 - sigma*sqrt(expiration)
    if play is 'call':
        return stock_price * stats.norm.cdf(d1) - strike_price * exp(-risk_free_rate * expiration) * stats.norm.cdf(d2)
    elif play is 'put':
        return -stock_price * stats.norm.cdf(-d1) + strike_price * exp(-risk_free_rate * expiration)*stats.norm.cdf(-d2)
    else:
        raise AttributeError


# if we want to calculate VaR for tomorrow
# start/end dates are datetimes, cl = confidence level, investment is the investment
def value_at_risk(investment, start_date, end_date, symbol, position, cl, n=None):
    stock_data = get_data('yahoo', symbol, start_date, end_date)
    mu = np.mean(stock_data['returns'])
    sigma = np.std(stock_data['returns'])
    alpha = norm.ppf(1 - cl)
    if n:
        var = investment * (mu * n - sigma * alpha * np.sqrt(n))
    else:
        var = position * (mu - sigma * alpha)
    return var


def capm(start_date, end_date, ticker1, ticker2):
    risk_free_rate = 0.05

    # get the data from Yahoo Finance
    stock1 = pdr.get_data_yahoo(ticker1, start_date, end_date)
    stock2 = pdr.get_data_yahoo(ticker2, start_date, end_date)

    # we prefer monthly returns instead of daily returns
    return_stock1 = stock1.resample('M').last()
    return_stock2 = stock2.resample('M').last()

    # creating a dataFrame from the data - Adjusted Closing Price is used as usual
    data = pd.DataFrame({'s_adjclose': return_stock1['Adj Close'], 'm_adjclose': return_stock2['Adj Close']},
                        index=return_stock1.index)
    # natural logarithm of the returns
    data[['s_returns', 'm_returns']] = np.log(
        data[['s_adjclose', 'm_adjclose']] / data[['s_adjclose', 'm_adjclose']].shift(1))
    # no need for NaN/missing values values so let's get rid of them
    data = data.dropna()

    # covariance matrix: the diagonal items are the vairances - off diagonals are the covariances
    covmat = np.cov(data["s_returns"], data["m_returns"])

    # calculating beta according to the formula
    beta = covmat[0, 1] / covmat[1, 1]

    # using linear regression to fit a line to the data [stock_returns, market_returns] - slope is the beta
    beta, alpha = np.polyfit(data["m_returns"], data['s_returns'], deg=1)

    # calculate the expected return according to the CAPM formula
    expected_return = risk_free_rate + beta * (data["m_returns"].mean() * 12 - risk_free_rate)
    return expected_return
    # example call: capm('2011-01-01', '2017-01-01','IBM', '^GSPC')


def create_dataset(dataset, metricone, metrictwo, comparator, model_name):

    # Use the prior two days of returns as predictor
    # values, with direction as the response
    X = dataset[metricone]
    y = dataset[metrictwo]

    # Create training and test sets
    X_train = X[X.index < comparator]
    X_test = X[X.index >= comparator]
    y_train = y[y.index < comparator]
    y_test = y[y.index >= comparator]

    # we use Logistic Regression as the machine learning model
    if model_name is 'LogReg':
        model = LogisticRegression()
    elif model_name is 'KNC':
        model = KNeighborsClassifier(300)
    elif model_name is 'SVC':
        model = LinearSVC()
    else:
        raise InvalidModelError('The Model must be one of: LogReg, KNC, SVC')
    # train the model on the training set
    model.fit(X_train, y_train)
    # make an array of predictions on the test set
    pred = model.predict(X_test)
    return [model.score(X_test, y_test), confusion_matrix(pred, y_test)]



