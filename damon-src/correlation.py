import numpy as np
import pandas as pd
# package imports
from visual import scatter, linear


def correlation(mainset, main_ticker, compset, comp_ticker, visual=None):
    if visual:
        corr_set = pd.DataFrame
        corr_set['Correlation'] = mainset.rolling_corr(compset)
        if visual is 'linear':
            linear(corr_set['Correlation'], f"{main_ticker + '-' + comp_ticker + 'Correlation'}", 'Time', 'Correlation')
        elif visual is 'scatter':
            scatter(mainset, main_ticker, compset, comp_ticker)
    return np.corrcoef(mainset, compset)[0, 1]
