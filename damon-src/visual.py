import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# package imports

# method for sequence of things common within all charts ot avoid repeated code


def linear(dataset, ticker, x_label, y_label):
    dataset.plot()
    plt.legend()
    plt.title(ticker)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # plt.savefig(filepath)
    plt.show()


def scatter(x, y, x_ticker, y_ticker):
    # line of best fit, correlation, other analyses (removable)
    plt.scatter(x, y)
    plt.xlabel(x_ticker)
    plt.ylabel(y_ticker)
    plt.legend()
    # plt.savefig(filepath)
    plt.show()


def noise(dataset, ticker):
    noisy_data = pd.DataFrame(np.random.normal(1.0, 0.03, (100, 10)))
    projections = noisy_data.cumprod()
    projections[ticker] = dataset
    projections.plot()
    # plt.savefig(filepath)
    plt.show()
