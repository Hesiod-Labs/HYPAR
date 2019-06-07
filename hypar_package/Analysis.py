from hypar_package import Portfolio
from hypar_package import Stock

import scipy.stats as stats
import numpy as np
import pandas as pd
import copy

def spearman_corr_coeffs(portfolio, attribute='changePercent'):
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

def mean_spearman_corr_coeffs(portfolio, attribute='changePercent'):
	pass

def weighted_ranked_spearman_coeffs(portfolio):
    
    """ Calculate the Spearman rank correlation coefficients (SRCC) of all
    Stocks in the Portfolio, weighted by their rank amongst all other
    pairwise correlation coefficients, and normalized by the number of 
    Stocks.

    If there are N Stocks, then an N x N DataFrame is constructed such that 
    the ij-th entry is the SRCC between Stock i and Stock j. Excluding the 
    1s along the diagonal, the N x N matrix is converted to another DataFrame
    that lists all pairs of Stocks and their respective SRCC.

    These values are then sorted in accordance with their SRCC such that the
    ij-th and ji-th entries (i not equal to j) from the initial matrix are listed
    next to each other.

    Since the SRCC for the ij-th and ji-th entries are the same, they are assigned
    identical ranks. Thus, the highest rank is (N*2 - 1). Weighted coefficients are
    calculated by multiplying the rank value by the SRCC.

    The Stock pairs are then reorganized such that they are grouped by column "stock_i,"
    and all columns are then summed to generate a summed SRCC, summed rank, and summed 
    weighted coefficient for each Stock.

    A new column is finally added that normalizes the weighted coefficients by the number
    of Stocks in the Portfolio.

    Returns:
    	Dictionary form of the final table with each Stock's summed SRCC, rank, weighted
    	coefficients, and normalized coefficients.
    """

    # Create a copy of the portfolio so as not to modify the original
    port = copy.deepcopy(portfolio)

    # Calculate the Spearman rank correlation coefficients for each pair of Stocks
    initial_matrix = spearman_corr_coeffs(port)
    
    # Create the tabular list of Stock pairs and their correlation coefficients
    # Does not include each Stock with itself
    table = []
    for i in range(len(initial_matrix)):
        for j in range(len(initial_matrix)):
            if i is not j:
                stock_i = initial_matrix.index[i]
                stock_j = initial_matrix.index[j]
                coeff = initial_matrix.values[i][j]
                table.append([stock_i, stock_j, coeff])
    
    # Store this data as a DataFrame
    corr_matrix_list = pd.DataFrame(table, columns=['stock_i', 'stock_j', 'coeff'])
    
    # Arrange the pairs so that they are sorted by the coefficients
    # They are listed so that every two rows corresponds to the same coefficient
    corr_matrix_list = corr_matrix_list.sort_values(by='coeff', axis=0)
   
    
    # Add the numerical rankings to the table as a new column
    # Since the coefficients are identical for pairs, there are two of every rank
    coeff_ranks = []
    for i in enumerate(corr_matrix_list['coeff']):
    	coeff_ranks.append(i[0]//2 + 1)
    corr_matrix_list['ranked coeff'] = coeff_ranks

    # Calculate the weighted coefficients (determined by multiplying the rank by the coefficient)
    corr_matrix_list['weighted coeff'] = corr_matrix_list['coeff']*corr_matrix_list['ranked coeff']
    
    # Group the Stocks by the left-most Stock column of the table 
    corr_matrix_list = corr_matrix_list.sort_values(by='stock_i', axis=0)
  
    # Sum each group for every Stock to obtain the summed rank and summed unweighted, weighted,
    # and normalized coefficient (determined by the number of Stocks in the Portfolio)
    summed = corr_matrix_list.groupby(corr_matrix_list.index//(len(initial_matrix)-1)).sum()
    summed = summed.rename(columns= {'coeff' : 'summed coeff', 'ranked coeff' : 'summed rank'})
    summed['normalized weights'] = summed['weighted coeff']/(len(initial_matrix)-1)
    summed = summed.set_index(initial_matrix.index)
    summed = summed.sort_values('normalized weights', ascending=False)
    print(summed)
    
    return summed.to_dict()

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

