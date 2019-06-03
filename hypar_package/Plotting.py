from hypar_package import Portfolio
from hypar_package import Stock
from hypar_package import Analysis

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import numpy as np

def timeseries(portfolio, attribute, tickers, plot_title=None):

    port_ticks  = portfolio.list_tickers()

    data = []
    labels = []
    
    for t in tickers:
        if t in port_ticks:
            data.append(portfolio.get_stock(t).price_data[attribute])
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
    
    r = portfolio.get_stock(ticker).price_data[attribute]  
    ax = sns.distplot(r,
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