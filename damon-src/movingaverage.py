import pandas as pd
import matplotlib.pyplot as plt
# package imports


# only accepting closing prices
def add_moving_avg(dataset, day):
    # raise exception if the data is already in the table
    rolling_data = pd.DataFrame(dataset)
    rolling_data[f'{day}'] = dataset.rolling(day).mean()
    rolling_data.plot()
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'Rolling {str(day)}-Day Moving Average')
    plt.legend(loc='best')
    plt.show()


# def remove_moving_avg(dataset, day)
    # raise exception if the data does not exist in this table
