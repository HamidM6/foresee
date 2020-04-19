"""
sarimax from statsmodels
"""

import statsmodels.api
import numpy

def fit_sarimax(data_param_dict):
    
    model = 'sarimax'

    if time_grain == 'week':
        order = (0,0,1)
        s = 52
        seasonal_order = (0,0,0,s)
        trend = 'c'
        
    elif time_grain == 'month':
        exog = [None, None]
        order = (1,1,1)
        s = 12
        seasonal_order = (0,1,0,s) if len(input_endog) > 17 else (0,0,0,s)
        trend = 'n'
    
    try:
        
        sarimax_model = statsmodels.api.tsa.statespace.SARIMAX(
                                                                    endog = input_endog,
                                                                    exog = exog[0],
                                                                    order = order,
                                                                    seasonal_order = seasonal_order,
                                                                    trend = trend
                                                               ).fit()
        
        sarimax_fittedvalues = sarimax_model.fittedvalues.clip(lower=0)
        sarimax_forecast = sarimax_model.predict(
                                                    start = input_length,
                                                    end = input_length + forecast_length - 1,
                                                    exog = exog[1]
                                                 ).clip(lower=0)
        err = None
        
    except Exception as e:
        k
        sarimax_model = None
        sarimax_fittedvalues = None
        sarimax_forecast = None
        err = str(e)
        
    return sarimax_model, sarimax_fittedvalues, sarimax_forecast, err
