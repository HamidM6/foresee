"""
Holt-Winters
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# local module
from foresee.models import models_util

def holt_winters_fit_forecast(ts, fcst_len, freq):
    
    try:                           
        hw_model = ExponentialSmoothing(
                                            endog = ts,
                                            trend = 'add',
                                            damped = True,
                                            seasonal = 'add',
                                            seasonal_periods = freq
                                          ).fit(
                                                optimized = True
                                               )

        hw_fittedvalues = hw_model.fittedvalues    

        hw_forecast = hw_model.predict(
                                            start = len(ts),
                                            end =   len(ts) + fcst_len - 1
                                        )
        err = None
        
    except Exception as e:
        hw_fittedvalues = None
        hw_forecast = None
        err = str(e)
    
    
    return hw_fittedvalues, hw_forecast, err

def fit_holt_winters(data_dict, freq, fcst_len, model_params, run_type, epsilon):
    
    model = 'holt_winters'
    hw_params = model_params[model]
    complete_fact = data_dict['complete_fact']
    
    # dataframe to hold fitted values
    fitted_fact = pd.DataFrame()
    fitted_fact['y'] = complete_fact['y']
    fitted_fact['data_split'] = complete_fact['data_split']
    
    # dataframe to hold forecast values
    forecast_fact = pd.DataFrame()
    forecast_fact['y'] = np.full(fcst_len, 0)
    forecast_fact['data_split'] = np.full(fcst_len, 'Forecast')
    
    fit_fcst_fact = pd.concat([fitted_fact, forecast_fact], ignore_index=True)
    
    hw_wfa = None
    
    
    hw_fitted_values, hw_forecast, err = holt_winters_fit_forecast(
                                                                       ts = complete_fact['y'],
                                                                       fcst_len = fcst_len,
                                                                       freq = freq,
                                                                  )
    
    if run_type in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']    
        fitted_values, forecast, err = holt_winters_fit_forecast(
                                                                           ts = train_fact['y'],
                                                                           fcst_len = len(test_fact),
                                                                           freq = freq,
                                                                 )
        
        if err is None:
            hw_wfa = models_util.compute_wfa(
                                    y = test_fact['y'].values,
                                    yhat = forecast.values,
                                    epsilon = epsilon,
                                )
            hw_fitted_values = fitted_values.append(forecast, ignore_index=True)
            
        else:
            hw_wfa = -1
            
    if err is None:
        fit_fcst_fact['holt_winters_forecast'] = hw_fitted_values.append(hw_forecast).values
        fit_fcst_fact['holt_winters_wfa'] = hw_wfa
        
    else:
        fit_fcst_fact['holt_winters_forecast'] = 0
        fit_fcst_fact['holt_winters_wfa'] = -1
        

            
    return fit_fcst_fact, hw_wfa, err




