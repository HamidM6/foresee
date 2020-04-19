"""
exponentially weighted moving average
"""

import numpy
import pandas

def fit_ewm(data_param_dict):
    
    model = 'ewm_model'
    
    if time_grain == 'month':
        span = 2
    else:
        span = 4
    try:
        
        ewm_model = input_endog.ewm(span=span)
        ewm_fittedvalues = numpy.round(ewm_model.mean())
        
        ewm_forecast = numpy.empty(forecast_length)
        ewm_forecast.fill(ewm_fittedvalues.iloc[-1])
        ewm_forecast = pandas.Series(ewm_forecast)
        err = None

    except Exception as e:
        
        ewm_model = None
        ewm_fittedvalues = None
        ewm_forecast = None
        err = str(e)
        
    return ewm_model, ewm_fittedvalues, ewm_forecast, err