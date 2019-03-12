import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# package imports


def visual_main(dataset, ):


    dataset['Adj Close'].plot()
    # create legend with plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Price')
    # plt.title('NVDA')
    plt.show()

    # rolling 20, 80
    dataset['Rolling 50'] = dataset['Adj Close'].rolling(50).mean()
    dataset['Rolling 200'] = dataset['Adj Close'].rolling(200).mean()
    dataset[['Adj Close', 'Rolling 50', 'Rolling 200']].plot()
    plt.show()


    # scatter two data sets together
    # plot and return the correlation
    plt.scatter(x, y)
    plt.show()


    # there is also np.linspace()
    plt.hist(x, bins=100)
    plt.show()


def noise():
    returns = pd.DataFrame(np.random.normal(1.0, 0.03, (100, 10)))
    prices = returns.cumprod()
    prices.plot()
    plt.show()


def plot_percent_changes(dataset):
    dataset['Percent Change'].plot()
    plt.xlabel('Time')
    plt.ylabel('Percent')
    plt.show()


if __name__ == '__main__':
    visual_main()
