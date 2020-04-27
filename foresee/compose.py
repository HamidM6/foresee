# -*- coding: utf-8 -*-
"""
manage input and output of forecasting models
"""

import pandas as pd
import numpy as np
import datetime
import fitter



def model_fit(raw_fact, model_params, param_config, gbkey):
    
    freq = param_config['FREQ']
    forecast_len = param_config['FORECAST_LEN']
    
    model_list = param_config['MODEL_LIST']
    
    fit_result_list = list()
    
    data_param_list = _transform_dataframe_to_dict(raw_fact, gbkey)
    
    for data_param in data_param_list:
        
        df = data_param['df']
        
        fit_result = dict()
        
        fit_result['ts_id'] = data_param['ts_id']
        
        for m in model_list:

            f = fitter.fitter(m)

            (
            fit_result[m+'_modelobj'],
             fit_result[m+'_fitted_values'],
             fit_result[m+'_forecast'],
             fit_result[m+'_err']
             ) = f.fit(df, freq, forecast_len, model_params)
            
        fit_result_list.append(fit_result)
        
    return fit_result_list


def _transform_dataframe_to_dict(raw_fact, gbkey):
    
    data_param_list = list()
    
    if gbkey is None:
        
        data_param_list.append({'ts_id':1, 'df':raw_fact})
    
    else:
        for k,v in raw_fact.groupby(gbkey):
            data_param_list.append({'ts_id':k, 'df':v})
    
    return data_param_list



def transform_dict_to_df(fit_result_list, model_list):
    
    df_list = list()
    
    for v in fit_result_list:
        
        df = pd.DataFrame()
     
        for m in model_list:

            try:
                fcst = v[m+'_fitted_values'].append(v[m+'_forecast']).values

                df[m+'_forecast'] = fcst

            except Exception as e:
                df[m+'_forecast'] = 0
                print(str(e))
                
        df['ts_id'] = v['ts_id']
        df_list.append(df)
        
    result = pd.concat(df_list, axis=0, ignore_index=True) 
    
    return result


