"""
collection of utility functions used in models section
"""

import numpy as np

def compute_wfa(y, yhat, epsilon):
    
    """
    weighted forecast accuracy
    """
    
    try:
        abs_err = compute_abs_err(y, yhat)
        wfa = max(0, 1-(2*sum(abs_err))/(sum(y) + sum(yhat) + epsilon))
        
    except Exception as e:
        raise ValueError('error call from wfa func: ' + str(e))
    
    return wfa

def compute_abs_err(y, yhat):
    
    #TODO: add more checks, e.g. data-type, same length, ...
    
    if any(np.isnan(y)) or any(np.isnan(yhat)):
        raise ValueError('error call from abs_err func: y or yhat has null values')
        
    if len(y) == 0 or len(yhat)  == 0:
        raise ValueError('error call from abs_err func: y or yhat is empty')
        
    return abs(y - yhat)


