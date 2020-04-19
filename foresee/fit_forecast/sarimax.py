"""
sarimax from statsmodels
"""

import statsmodels.api

def fit_sarimax(ts, freq, forecast_len, model_params):
    
    model = 'sarimax'
    sarimax_params = model_params[model]
    
    try:
        
        sarimax_model = statsmodels.api.tsa.statespace.SARIMAX(
                                                                    endog = ts,
                                                               ).fit()
        
        sarimax_fittedvalues = sarimax_model.fittedvalues
        sarimax_forecast = sarimax_model.predict(
                                                    start = len(ts),
                                                    end = len(ts) + forecast_len - 1,
                                                 )
        err = None
        
    except Exception as e:
        
        sarimax_model = None
        sarimax_fittedvalues = None
        sarimax_forecast = None
        err = str(e)
        
    return sarimax_model, sarimax_fittedvalues, sarimax_forecast, err
