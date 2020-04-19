# -*- coding: utf-8 -*-
"""
manage input and output of forecasting models
"""

import foresee.fitter

def model_fit(ts_fact, model_params, param_config):
    
    ts = ts_fact['ts']
    ts_id = ts_fact['ts_id']
    
    freq = param_config['freq']
    forecast_len = param_config['forecast_len']
    
    model_list = param_config['model_list']
    
    fit_result = dict()
    
    for m in model_list:
        
        f = foresee.fitter.fitter(m)
        
        (
                fit_result[m+'_modelobj'],
                 fit_result[m+'_fitted_values'],
                 fit_result[m+'_forecast'],
                 fit_result[m+'_err']
         ) = f.fit(ts, freq, forecast_len, model_params)
        
        
    return {ts_id: fit_result}

