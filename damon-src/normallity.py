from scipy import stats
import numpy as np
import matplotlib.pyplot as plt


# test if the distribution has skewness or kurtosis
def jarque_bera_test(dataset):
    # is p-value > 0.05 the data is most likely
    print(stats.jarque_bera(dataset)[1] < 0.05)
    return [stats.jarque_bera(dataset)[1], stats.skew(dataset), stats.kurtosis(dataset)]
