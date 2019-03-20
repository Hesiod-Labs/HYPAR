from scipy import exp, stats, log, sqrt


# play is call or put
def blackscholes(stock_price, strike_price, expiration, risk_free_rate, sigma, play):
    d1 = (log(stock_price/strike_price)+(risk_free_rate+sigma*sigma/2.0)*expiration)/(sigma*sqrt(expiration))
    d2 = d1 - sigma * sqrt(expiration)
    if play is 'call':
        return stock_price * stats.norm.cdf(d1) - strike_price * exp(-risk_free_rate * expiration) * stats.norm.cdf(d2)
    elif play is 'put':
        return -stock_price * stats.norm.cdf(-d1) + strike_price * exp(-risk_free_rate * expiration)*stats.norm.cdf(-d2)
    else:
        raise AttributeError

# wikipedia links
# https://en.wikipedia.org/wiki/Valuation_of_options
# https://en.wikipedia.org/wiki/Black_model
# https://en.wikipedia.org/wiki/Lattice_model_(finance)
# https://en.wikipedia.org/wiki/Monte_Carlo_methods_for_option_pricing
# https://en.wikipedia.org/wiki/Finite_difference_methods_for_option_pricing
# https://en.wikipedia.org/wiki/Heston_model
# https://en.wikipedia.org/wiki/Heath%E2%80%93Jarrow%E2%80%93Morton_framework
# https://en.wikipedia.org/wiki/Variance_gamma_process
# http://pages.hmc.edu/evans/e136l9.pdf
