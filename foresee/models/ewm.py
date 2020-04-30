"""
exponentially weighted moving average
"""

import numpy as np
import pandas as pd

# local module
import models_util

def ewm_fit_forecast(ts, fcst_len, span):
    
    try:
        
        ewm_model = pd.Series(ts).ewm(span=span)
        ewm_fittedvalues = ewm_model.mean()
        
        ewm_forecast = np.empty(fcst_len)
        ewm_forecast.fill(ewm_fittedvalues.iloc[-1])
        ewm_forecast = pd.Series(ewm_forecast)
        err = None

    except Exception as e:
        
        ewm_fittedvalues = None
        ewm_forecast = None
        err = str(e)
        
    return ewm_fittedvalues, ewm_forecast, err    

def fit_ewm(data_dict, freq, fcst_len, model_params, run_type, epsilon):
    
    model = 'ewm_model'
    ewm_params = model_params[model]
    span = 5
    
    complete_fact = data_dict['complete_fact']
    ewm_wfa = None
    
    ewm_fitted_values, ewm_forecast, err = ewm_fit_forecast(
                                                        ts = complete_fact['y'],
                                                        fcst_len = fcst_len,
                                                        span = span,

                                                    )
    
    
    if run_type in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        fitted_values, forecast, err = ewm_fit_forecast(
                                                            ts = train_fact['y'],
                                                            fcst_len = len(test_fact) ,
                                                            span = span
                                                        )
        
        if err is None:
            ewm_wfa = models_util.compute_wfa(
                                    y = test_fact['y'].values,
                                    yhat = forecast.values,
                                    epsilon = epsilon,
                                )
            ewm_fitted_values = fitted_values.append(forecast)
            
        else:
            ewm_wfa = -1
            
    return ewm_fitted_values, ewm_forecast, ewm_wfa, err







