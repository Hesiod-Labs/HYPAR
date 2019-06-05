from hypar_package import Portfolio
from hypar_package import Stock

import scipy.stats as stats
import numpy as np
import pandas as pd
import copy

def spearman_corr_coeffs(portfolio, attribute='close'):

	col = []

	port = copy.deepcopy(portfolio)

	for s_i in port.stocks:
		row = []
		
		for s_j in port.stocks:
			coeff, pval = stats.spearmanr(s_j.price_data[attribute], 
				s_i.price_data[attribute])
			row.append(coeff)

		col.append(row)

	corr_matrix = pd.DataFrame(col, columns=port.list_tickers())
	corr_matrix.index = port.list_tickers()

	return corr_matrix

def mean_spearman_corr_coeffs(portfolio, attribute='close'):
	pass

def reduce_spearman_corr_matrix():
	pass

def compare_corr_matrices():
	pass

def moments(portfolio, ticker, attribute='close', bias_correction=True):
	
	if ticker in portfolio.list_tickers():
		data = portfolio.get_stock(ticker).price_data[attribute].values
		mean = np.mean(data)
		var = np.var(data)
		sk = stats.skew(data, bias=not bias_correction)
		kurt = stats.kurtosis(data, bias=not bias_correction)
		jb_test = stats.jarque_bera(data)[1] > 0.05

	return {'mean':mean, 
	'variance':var, 
	'skew':sk, 
	'kurtosis':kurt, 
	'jarque bera':jb_test}

def asksr():
	pass

