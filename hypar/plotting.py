from hypar import portfolio
from hypar import stock
from hypar import analysis
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import scipy.stats as stats
import numpy as np

def time_series(portfolio, tickers, data_source=price_data, attribute='close',
				start_date=None, end_date=None, plot_title=None):
	"""Plot a time series of a Stock's attributes with optional start and end
	date specifications. Additionally, a plot title can be added as an input
	parameter.

	Stocks are specified by their tickers as a list of strings. Of those Stocks
	that are also present in the Portfolio, the data is acquired and added to a
	list to be plotted. If start and/or end	dates are specified, the data is
	sliced to only plot that date range.

	Args:
		portfolio: Portfolio that contains the Stocks to be plotted
		tickers: Stock symbols that belong to the portofolio specified
		attribute: String that

	Returns:
		seaborn line plot
	"""
	# Used to store the Stock data to plot
	data = []

	# Used to store the Stock tickers for the plot legend
	labels = []

	for t in tickers:
		# If the Stock exists in the Portfolio...
		if t in portfolio.list_tickers():
			# gather the data associated with the input attribute
			stock_data = portfolio.get_stock(t).data_source[attribute]
			# If either start or end dates are specified, slice the data
			if start_date is not None:
				stock_data = stock_data[start_date:]
			if end_date is not None:
				stock_data = stock_data[:end_date]
			# Add the Stock data to the list to be potted
			data.append(stock_data)
			# Add the ticker to be added to the legend
			labels.append(t)
	# Set the index for the DataFrame to be the datetime index of the Stock(s)
	index = data[0].index
	# Create a DataFrame to add the data to plot
	plot_df = pd.DataFrame(index=index)
	# Add the Stock data to the DataFrame and label the columns by ticker
	for d, t in zip(data, labels):
	    plot_df[t] = d.values
	# Create a seaborn lineplot with all the Stock data
	ax = sns.lineplot(data=plot_df)
	# Prevent datetime tick marks from overlapping
	ax.xaxis.set_major_locator(plt.MaxNLocator(5))
	# Set the x, y labels
	ax.set(xlabel='Date', ylabel= attribute.capitalize())
	# Set the plot title, if specifieds
	ax.set_title(plot_title)

	return ax

def cdf(portfolio, ticker, data_source=price_data, attribute='changePercent'):
	"""Plot a cumulative distribution function of a Stock's data belonging to
	a specific Portfolio.

	Returns:
		seaborn cumulative distribution function plot
	"""
	# Create a seaborn CDF plot for the Stock data
	ax = sns.distplot(
					portfolio.get_stock(ticker).data_source[attribute],
					rug=True,
                    hist_kws=dict(cumulative=True),
                    kde_kws=dict(cumulative=True))
	# Modify the title and x,y labels
    ax.set_title(ticker + ' CDF')
    ax.set_ylabel('Density')
    ax.set_xlabel(attribute.capitalize())

    return ax

def spearman_corr_heatmap(portfolio, data_source=price_data,
	attribute='changePercent', absolute=True):
	"""Create a heatmap of the Spearman rank correlation coefficients based on
	the Stock attribute specified.

	Returns:
		seaborn heatmap of correlation coefficients
	"""
	matrix = Analysis.spearman_corr_coeffs(portfolio, data_source, attribute)

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
