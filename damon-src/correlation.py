import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import timedelta
# package imports
from exceptions import InvalidCorrelationFormattingError
from tutor import days_between, percent_change

# inputs: variable number of datasets preferably a dataset of entirely comparable columns
# time period, what they want returned, plot type

# can either do this independently or go to a page and have the information set automatically

# correlation between one main dataset and a variable amount of others

# model either price or pecent change
def correlation_main(main_name, comp_name, start_date, end_date, visual):
    # inputs
    mainset = get_data(main_name, 'yahoo', start_date, end_date)['Adj Close']
    timespan = days_between(start_date, end_date)
    compset = get_data(comp_name, 'yahoo', start_date, end_date)['Adj Close']
    correlation = np.corrcoef(mainset, compset)[0, 1]

    # need a method that does the general consistent plot formatting
    # concatenate multiple datasets of the same column into one with all of their columns

    if visual is 'linear':
        # how to set the new column of data for correlations on specific days
        # what does .rolling() do
        plt.title(main_name + ' vs. ' + comp_name + ': ' + str(correlation))
        plt.show()

    elif visual is 'scatter':

        plt.scatter(mainset['Adj Close'], compset['Adj Close'])
        plt.xlabel(main_name)
        plt.ylabel(comp_name)
        # plt.text(60, .025, f'Correlation: {correlation}')
        plt.savefig(f'/Users/connormcmurry/Desktop/Hesiod Financial/hLabs/HYPAR/broker/broker-src/{main_name}-corr.pdf')
        plt.show()


if __name__ == '__main__':
    correlation_main()
