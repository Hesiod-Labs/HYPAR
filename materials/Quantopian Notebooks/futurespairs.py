import itertools

import numpy as np
import pandas as pd
import scipy as sp
from statsmodels.tsa.stattools import coint

from quantopian.algorithm import order_optimal_portfolio
import quantopian.optimize as opt

month_idx = 0

def initialize(context):
    # Quantopian backtester specific variables
    
    context.futures_pairs = [
        (
            continuous_future(
                'LC',
                offset=month_idx,
                roll='calendar',
                adjustment='mul',
            ),
            continuous_future(
                'FC',
                offset=month_idx,
                roll='calendar',
                adjustment='mul',
            ),
        ),
        (
            continuous_future(
                'CL',
                offset=month_idx,
                roll='calendar',
                adjustment='mul',
            ),
            continuous_future(
                'XB',
                offset=month_idx,
                roll='calendar',
                adjustment='mul',
            ),
        ),
        (
            continuous_future(
                'SM',
                offset=month_idx,
                roll='calendar',
                adjustment='mul',
            ),
            continuous_future(
                'BO',
                offset=month_idx,
                roll='calendar',
                adjustment='mul',
            ),
        ),
    ]
    
    context.futures_list = list(itertools.chain.from_iterable(context.futures_pairs))
    
    context.num_pairs = len(context.futures_pairs)
    # strategy specific variables
    context.long_ma = 63
    context.short_ma = 5
    
    context.inLong = {
        (pair[0].root_symbol, pair[1].root_symbol): False for pair in context.futures_pairs
    }
    context.inShort = {
        (pair[0].root_symbol, pair[1].root_symbol): False for pair in context.futures_pairs
    }
    
    context.long_term_weights = {cont_future.root_symbol: 0 for cont_future in context.futures_list}
    context.current_weights = {}
    
    schedule_function(func=rebalance_pairs, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=30))
    
# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    # Our work is now scheduled in check_pair_status
    pass

def rebalance_pairs(context, data):
    if get_open_orders():
        return
    
    prices = data.history(context.futures_list, 'price', context.long_ma, '1d')
     
    
    for future_y, future_x in context.futures_pairs:
        Y = prices[future_y]
        X = prices[future_x]
        
        y_log = np.log(Y)
        x_log = np.log(X)
        
        pvalue = coint(y_log, x_log)[1]
        if pvalue > 0.10:
            log.info(
                '({} {}) no longer cointegrated, no new positions.'.format(
                    future_y.root_symbol,
                    future_x.root_symbol,
                ),
            )
            continue
            
        regression = sp.stats.linregress(
            x_log[-context.long_ma:],
            y_log[-context.long_ma:],
        )
        
        spreads = Y - (regression.slope * X)

        zscore = (
            np.mean(spreads[-context.short_ma:]) - np.mean(spreads)
        ) / np.std(spreads, ddof=1)
            
        future_y_contract, future_x_contract = data.current(
            [future_y, future_x],
            'contract',
        )
        
        context.current_weights[future_y_contract] = context.long_term_weights[future_y_contract.root_symbol]
        context.current_weights[future_x_contract] = context.long_term_weights[future_x_contract.root_symbol]
        
        
        hedge_ratio = regression.slope
        
        if context.inShort[(future_y.root_symbol, future_x.root_symbol)] and zscore < 0.0:
            context.long_term_weights[future_y_contract.root_symbol] = 0
            context.long_term_weights[future_x_contract.root_symbol] = 0
            context.current_weights[future_y_contract] = context.long_term_weights[future_y_contract.root_symbol]
            context.current_weights[future_x_contract] = context.long_term_weights[future_x_contract.root_symbol]
                
            context.inLong[(future_y.root_symbol, future_x.root_symbol)] = False
            context.inShort[(future_y.root_symbol, future_x.root_symbol)] = False
            continue

        if context.inLong[(future_y.root_symbol, future_x.root_symbol)] and zscore > 0.0:
            context.long_term_weights[future_y_contract.root_symbol] = 0
            context.long_term_weights[future_x_contract.root_symbol] = 0
            context.current_weights[future_y_contract] = context.long_term_weights[future_y_contract.root_symbol]
            context.current_weights[future_x_contract] = context.long_term_weights[future_x_contract.root_symbol]
                
            context.inLong[(future_y.root_symbol, future_x.root_symbol)] = False
            context.inShort[(future_y.root_symbol, future_x.root_symbol)] = False
            continue

        if zscore < -1.0 and (not context.inLong[(future_y.root_symbol, future_x.root_symbol)]):
            # Only trade if NOT already in a trade
            y_target_contracts = 1
            x_target_contracts = hedge_ratio
            context.inLong[(future_y.root_symbol, future_x.root_symbol)] = True
            context.inShort[(future_y.root_symbol, future_x.root_symbol)] = False

            (y_target_pct, x_target_pct) = computeHoldingsPct(
                y_target_contracts,
                x_target_contracts, 
                future_y_contract.multiplier * Y[-1],
                future_x_contract.multiplier * X[-1]
            )
            
            context.long_term_weights[future_y_contract.root_symbol] = y_target_pct
            context.long_term_weights[future_x_contract.root_symbol] = -x_target_pct
            context.current_weights[future_y_contract] = context.long_term_weights[future_y_contract.root_symbol]
            context.current_weights[future_x_contract] = context.long_term_weights[future_x_contract.root_symbol]
            continue

        if zscore > 1.0 and (not context.inShort[(future_y.root_symbol, future_x.root_symbol)]):
            # Only trade if NOT already in a trade
            y_target_contracts = 1
            x_target_contracts = hedge_ratio
     
            context.inLong[(future_y.root_symbol, future_x.root_symbol)] = False
            context.inShort[(future_y.root_symbol, future_x.root_symbol)] = True
            
            (y_target_pct, x_target_pct) = computeHoldingsPct(
                y_target_contracts,
                x_target_contracts, 
                future_y_contract.multiplier * Y[-1],
                future_x_contract.multiplier * X[-1]
            )
            
            context.long_term_weights[future_y_contract.root_symbol] = -y_target_pct
            context.long_term_weights[future_x_contract.root_symbol] = x_target_pct
            context.current_weights[future_y_contract] = context.long_term_weights[future_y_contract.root_symbol]
            context.current_weights[future_x_contract] = context.long_term_weights[future_x_contract.root_symbol]
            continue
    
    adjusted_weights = pd.Series({
        k: v / (len(context.futures_pairs)) for k, v in context.current_weights.items()
    })
    
    order_optimal_portfolio(
        opt.TargetWeights(adjusted_weights),
        constraints=[
            opt.MaxGrossExposure(1.0),
        ],
    )
    log.info('weights: ', adjusted_weights)
        
    
def computeHoldingsPct(yShares, xShares, yPrice, xPrice):
    yDol = yShares * yPrice
    xDol = xShares * xPrice
    notionalDol =  abs(yDol) + abs(xDol)
    y_target_pct = yDol / notionalDol
    x_target_pct = xDol / notionalDol
    return (y_target_pct, x_target_pct)