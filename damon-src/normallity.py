from scipy import stats


def jarque_bera_test(dataset):
    # is p-value > 0.05 the data is most likely
    return stats.jarque_bera(dataset)[1]


def skewness(dataset):
    return stats.skew(dataset)


def kurtosis(dataset):
    return stats.kurtosis(dataset)
