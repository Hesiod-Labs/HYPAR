import operator
import numpy as np
import scipy.stats as stats
from hypar.portfolio import Portfolio


def correlation(portfolio, attribute='changePercent', method='spearman',
                absolute=True, weight_by_rank=False, weight_by_shares=False,
                coeffs_only=False, sort_by_ticker=False, sort_by_coeff=False,
                descending=False):
    def arrange(coeff_data, by_ticker=False, by_coeff=False, order=False):
        if by_ticker and by_coeff:
            coeff_data.sort(reverse=order, key=operator.itemgetter(0, 2))
        if by_ticker and not by_coeff:
            coeff_data.sort(reverse=order, key=operator.itemgetter(0))
        if by_coeff and not by_ticker:
            coeff_data.sort(reverse=order, key=operator.itemgetter(2))
        return coeff_data

    def normalize(data):
        raw = np.array([x[2] for x in data])
        for i, v in enumerate(data):
            data[i][2] = raw[i] / raw.sum()
        return data

    methods = {'pearson': stats.pearsonr,
               'spearman': stats.spearmanr,
               'kendall': stats.kendalltau,
               'weighted kendall': stats.weightedtau}

    if method not in methods:
        raise ValueError(
            'Acceptable methods: "pearson," "spearman", "kendall", "weighted '
            'kendall"')

    corr_data = portfolio.get_data_slice(attribute, as_dict=False, dated=False)

    for i in corr_data:
        if i[1][0] == 0:
            i[1].remove(0)

    if absolute:
        coeffs = [[x[0], y[0], abs(methods[method](x[1], y[1])[0])]
                  for x in corr_data for y in corr_data]
    else:
        coeffs = [[x[0], y[0], methods[method](x[1], y[1])[0]]
                  for x in corr_data for y in corr_data]

    coeffs = arrange(coeffs, by_coeff=True)
    num_stocks = len(portfolio.stocks)
    coeffs = coeffs[:-num_stocks]

    if weight_by_rank:
        num_pairs = int((num_stocks ** 2) - num_stocks)
        ranks = np.arange(1, int((num_pairs + 1) / 2) + 1).repeat(2)
        for i, r in enumerate(zip(coeffs, ranks)):
            coeffs[i][2] = coeffs[i][2] * r[1]

    if weight_by_shares:
        for i, v in enumerate(coeffs):
            s1 = portfolio.stocks[v[0]].num_shares[portfolio]
            s2 = portfolio.stocks[v[1]].num_shares[portfolio]
            coeffs[i][2] = coeffs[i][2] * (s1 + s2)

    coeffs = normalize(coeffs)
    coeffs = arrange(coeffs, sort_by_ticker, sort_by_coeff, descending)

    if coeffs_only:
        return [c[2] for c in coeffs]

    return coeffs


# TODO Add as parameter to correlation method
def mean_spearman_corr_coeffs(portfolio: Portfolio,
                              existing_matrix=None,
                              attribute='changePercent',
                              absolute=True):
    pass


# TODO Add docstring and merge with new correlation method
def weighted_ranked_spearman_coeffs(portfolio: Portfolio,
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
    pass


def reduced_corr_portfolio(portfolio: Portfolio,
                           attribute='changePercent',
                           absolute=True):
    """Using a copy of the Portfolio, the normalized, weighted Spearman rank
    correlation coefficients are calculated. The Stock with the highest
    coefficient is removed from the Portfolio.

    Returns:
        A tuple with the first element being the ticker of the Stock removed
        from the Portfolio, and the second element being a copy of the Portfolio
        without the Stock that was removed.
    """
    pass


def moments(portfolio, ticker, attribute='close', bias_correction=True):
    """ Calculate the first, second, third, and fourth statistical moments
    of a Stock's attribute data.

    Also determine if the data is normally distributed by applying the
    Jarque-Bera test. If the p-value is greater than 0.05, the data is
    normally distributed.
    """

    if ticker in portfolio.stocks.keys():
        data = portfolio.get_stock(ticker).price_data[attribute].values()
        mean = np.mean(data)
        var = np.var(data)
        sk = stats.skew(data, bias=not bias_correction)
        kurt = stats.kurtosis(data, bias=not bias_correction)
        jb_test = stats.jarque_bera(data)[1] > 0.05

    return {'mean': mean,
            'variance': var,
            'skew': sk,
            'kurtosis': kurt,
            'jarque bera': jb_test}


def asksr():
    pass
