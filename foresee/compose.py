# -*- coding: utf-8 -*-
"""
manage input and output of forecasting models
"""

import fitter

def model_fit(ts_list, model_params, param_config):
    
    freq = param_config['freq']
    forecast_len = param_config['forecast_len']
    
    model_list = param_config['model_list']
    
    fit_result_list = list()
    
    for ts_dict in ts_list:
        
        fit_result = dict()
        fit_result['ts_id'] = ts_dict['ts_id']
        
        ts = ts_dict['ts']

        for m in model_list:

            f = fitter.fitter(m)

            (
            fit_result[m+'_modelobj'],
             fit_result[m+'_fitted_values'],
             fit_result[m+'_forecast'],
             fit_result[m+'_err']
             ) = f.fit(ts, freq, forecast_len, model_params)
            
        fit_result_list.append(fit_result)
        
    return fit_result_list

