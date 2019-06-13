from hypar_package import Portfolio
from hypar_package import Stock
from hypar_package import Analysis

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import scipy.stats as stats
import numpy as np

def time_series(portfolio, tickers, attribute='close', start_date=None, end_date=None, plot_title=None):
	""" Plot a time series of a Stock's attributes with optional start and end date specificaiotns.
	Additionally, a plot title can be added as an input paramter.

	Stocks are specified by their tickers as a list of strings. Of those Stocks that are also present
	in the Portfolio, the data is acquired and added to a list to be plotted. If start and/or end
	dates are specified, the data is sliced to only plot that date range.

	Returns:
		matplotlib ax that is plotted.
	"""

	data = []
	labels = []

	for t in tickers:
		if t in portfolio.list_tickers():
			stock_data = portfolio.get_stock(t).price_data[attribute]
			if start_date is not None:
				stock_data = stock_data[start_date:]
			if end_date is not None:
				stock_data = stock_data[:end_date]
			data.append(stock_data)
			labels.append(t)

	index = data[0].index
	plot_df = pd.DataFrame(index=index)

	for d, t in zip(data, labels):
	    plot_df[t] = d.values

	ax = sns.lineplot(data=plot_df)
	ax.xaxis.set_major_locator(plt.MaxNLocator(5))
	ax.set(xlabel='Date', ylabel= attribute.capitalize())
	ax.set_title(plot_title)

	return ax

def cdf(portfolio, ticker, attribute='changePercent'):

    ax = sns.distplot(portfolio.get_stock(ticker).price_data[attribute],
                      rug=True,
                      hist_kws=dict(cumulative=True),
                      kde_kws=dict(cumulative=True))
    ax.set_title(ticker + ' CDF')
    ax.set_ylabel('Density')
    ax.set_xlabel(attribute.capitalize())

    return ax

def spearman_corr_heatmap(portfolio, attribute='changePercent'):

	matrix = Analysis.spearman_corr_coeffs(portfolio, attribute)

	mask = np.zeros_like(matrix)
	mask[np.triu_indices_from(mask)]=True
	ax = sns.heatmap(matrix,
	                 annot=True,
	                 mask=mask,
	                 cmap='bwr', vmin=-1, vmax=1)
	ax.set_title(f'Portfolio {attribute.capitalize()} Spearman Correlation Heat Map')

	return ax

def scatter_matrix():
	pass
