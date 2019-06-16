from hypar import portfolio
from hypar import stock
import scipy.stats as stats
import numpy as np
import pandas as pd
import copy
import itertools as iter

def spearman_corr_coeffs(portfolio,
						data_source=stock.Stock.price_data,
						attribute='changePercent',
						absolute=True):
	"""Calculate the Spearman rank correlation coefficient between every Stock
	in the Portfolio. If absolute is True, then the absolute value of the
	coefficients are calculated.

		Returns:
			NxN pandas DataFrame with N being the number of stocks in the
			Portfolio. The ij-th entry is the Spearman rank correlation
			coefficient between Stock i and Stock j.
	"""
	# Create an empty column to append coefficients
	col = []

	# Create a copy of the Portfolio
	port = copy.deepcopy(portfolio)

	# Iterate through the dictionary of Stocks in the Portfolio.
	# Calculate the Spearman rank correlation coefficient between
	# one Stock and every other Stock, and append this row to the
	# list of columns.
	for s_i in port.stocks.values():
		row = []

		for s_j in port.stocks.values():
			coeff, pval = stats.spearmanr(s_j.data_source[attribute],
										s_i.data_source[attribute])
			row.append(coeff)

		col.append(row)

	# Create a pandas DataFrame to store the coefficients.
	# Label the column and row indices by the Stock tickers.
	corr_matrix = pd.DataFrame(col, columns=port.stocks.keys())
	corr_matrix.index = port.stocks.keys()

    # If absolute is True, calculate the absolute value of the cofficents.
    corr_matrix = np.abs(corr_matrix) if absolute

	return corr_matrix

def mean_spearman_corr_coeffs(portfolio,
							data_source=price_data,
							attribute='changePercent'):
	pass

def weighted_ranked_spearman_coeffs(portfolio,
									data_source=stock.Stock.price_data,
									attribute='changePercent',
									absolute=True):

    """Calculate the Spearman rank correlation coefficients (SRCC) of all
    Stocks in the Portfolio, weighted by their rank amongst all other
    pairwise correlation coefficients, and normalized by the number of
    Stocks.If absolute is True, use the absolute value of the coefficients.

    If there are N Stocks, then an N x N DataFrame is constructed such that
    the ij-th entry is the SRCC between Stock i and Stock j. Excluding the
    1s along the diagonal, the N x N matrix is converted to another DataFrame
    that lists all pairs of Stocks and their respective SRCC.

    These values are then sorted in accordance with their SRCC such that the
    ij-th and ji-th entries (i not equal to j) from the initial matrix are
	listed next to each other.

    Since the SRCC for the ij-th and ji-th entries are the same, they are
	assigned identical ranks. Thus, the highest rank is (N(N - 1))/2. Weighted
	coefficients are calculated by multiplying the rank value by the SRCC.

    The Stock pairs are then reorganized such that they are grouped by column
	"stock_i," and all columns are then summed to generate a summed SRCC,
	summed rank, and summed weighted coefficient for each Stock.

    A new column is finally added that normalizes the weighted coefficients by
	the number of Stocks in the Portfolio.

    Returns:
    	Dictionary form of the final table with each Stock's summed SRCC, rank,
		weighted coefficients, and normalized coefficients.
    """
    # Create a copy of the portfolio so as not to modify the original.
    port = copy.deepcopy(portfolio)

    # Calculate the Spearman rank correlation coefficients for every Stock pair.
    initial_matrix = spearman_corr_coeffs(port, data_source=data_source,
										attribute=attribute,
										absolute=absolute,
										ranking_factor='normalized num shares')

    # Create the tabular list of Stock pairs and their correlation coefficients.
    # Does not include each Stock with itself.
    table = []
    for i in range(len(initial_matrix)):
        for j in range(len(initial_matrix)):
            if i is not j:
                stock_i = initial_matrix.index[i]
                stock_j = initial_matrix.index[j]
                coeff = initial_matrix.values[i][j]
                table.append([stock_i, stock_j, coeff])

    # Store this data as a DataFrame
    corr_matrix_list = pd.DataFrame(table,
									columns=['stock_i', 'stock_j', 'coeff'])

    # Arrange the pairs so that they are sorted by the coefficients.
    # They are listed so that every two rows corresponds to the same
	# coefficient.
    corr_matrix_list = corr_matrix_list.sort_values(by='coeff', axis=0)

    # Add the numerical rankings to the table as a new column.
    # Since the coefficients are identical for pairs, there are two of each
	# rank.
    coeff_ranks = []
    for i in enumerate(corr_matrix_list['coeff']):
    	coeff_ranks.append(i[0]//2 + 1)
	corr_matrix_list['ranked coeff'] = coeff_ranks

    # Calculate the weighted coefficients which is determined by multiplying
	# the rank by the coefficient.
	coeffs = corr_matrix_list['coeff']
	ranks = corr_matrix_list['ranked coeff']
    corr_matrix_list['weighted coeff'] = coeffs*ranks

    # Group the Stocks by the left-most Stock column of the table
    corr_matrix_list = corr_matrix_list.sort_values(by='stock_i', axis=0)

    # Sum each group for every Stock to obtain the summed rank and summed
	# unweighted, weighted, and normalized coefficient which is determined by
	# the number of Stocks in the Portfolio
    summed = corr_matrix_list.groupby(
				corr_matrix_list.index//(len(initial_matrix)-1)).sum()
    summed = summed.rename(columns= {'coeff' : 'summed coeff',
									'ranked coeff' : 'summed rank'})
    summed['normalized num stocks'] = summed['weighted coeff']/(len(initial_matrix)-1)
	summed['normalized num shares'] = summed['weighted coeff']/portfolio.total_shares()
    summed = summed.set_index(initial_matrix.index)
    summed = summed.sort_values(ranking_factor, ascending=False)
    print(summed)

    return summed.to_dict()

def reduced_corr_portfolio(portfolio, data_source=price_data,
							attribute='changePercent',  absolute=True):
    """Using a copy of the Portfolio, the normalized, weighted Spearman rank
	correlation coefficients are calculated. The Stock with the highest
	coefficient is removed from the Portfolio.

    Returns:
        A tuple with the first element being the ticker of the Stock removed
		from the Portfolio, and the second element being a copy of the Portfolio
		without the Stock that was removed.
    """

    # Create a copy of the Portfolio.
    port = copy.deepcopy(portfolio)

    # Calculate the absolute normalized, weighted Spearman rank correlation
	# coefficients.
    corr_table = weighted_ranked_spearman_coeffs(portfolio,
												data_source=data_source,
												attribute=attribute,
												absolute=absolute)

    # Obtain the ticker of the Stock with the highest correlation.
    stock_to_remove_ticker = list(weighted_ranked_spearman_coeffs(portfolio,
																data_source=data_source,
																attribute=attribute,
																absolute=absolute)['normalized weights'])[0]
    port.remove_stock(port.get_stock(stock_to_remove_ticker))
    return stock_to_remove_ticker, port

def compare_corr_matrices():
	pass

def moments(portfolio, ticker, data_source=price_data, attribute='close', bias_correction=True):
	""" Calculate the first, second, third, and fourth statistical moments
	of a Stock's attribute data.

	Also determine if the data is normally distributed by applying the
	Jarque-Bera test. If the p-value is greater than 0.05, the data is
	normally distributed.
	"""

	if ticker in portfolio.list_tickers():
		data = portfolio.get_stock(ticker).data_source[attribute].values
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
