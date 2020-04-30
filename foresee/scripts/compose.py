# -*- coding: utf-8 -*-
"""
manage input and output of forecasting models
"""

import pandas as pd
import numpy as np
import datetime
import fitter



def compose_fit(pre_processed_dict, model_params, param_config, gbkey, run_type):
    
    freq = param_config['FREQ']
    forecast_len = param_config['FORECAST_LEN']
    model_list = param_config['MODEL_LIST']
    epsilon = param_config['EPSILON']
    
    # list of dictionaries
    fit_result_list = list()
    
    for k, data_dict  in pre_processed_dict.items():
        
        fit_result = dict()
        
        fit_result['ts_id'] = k
        
        for m in model_list:

            f = fitter.fitter(m)

            (
             fit_result[m+'_fitted_values'],
             fit_result[m+'_forecast'],
             fit_result[m+'_wfa'],
             fit_result[m+'_err']
             ) = f.fit(data_dict, freq, forecast_len, model_params, run_type, epsilon)
            
        fit_result_list.append(fit_result)
        
    result = combine_to_dataframe(fit_result_list, model_list, run_type)
        
    return result, fit_result_list



def combine_to_dataframe(fit_result_list, model_list, run_type):
    
    #TODO: find the best model
    #TODO: return result

    if run_type == 'best_model':

        fit_result_list = _find_best_model(fit_result_list, model_list)
        
        df_list = list()

        for result_dict in fit_result_list:

            bm = result_dict['best_model']

            df = pd.DataFrame()

            try:
                fcst = result_dict[bm+'_fitted_values'].append(result_dict[bm+'_forecast']).values
                df[bm+'_forecast'] = fcst
                df[bm+'_wfa'] = result_dict[bm+'_wfa']

            except Exception as e:
                df[bm+'_forecast'] = 0
                df[bm+'_wfa'] = -1
                print(str(e))

            df['ts_id'] = result_dict['ts_id']
            df['best_model'] = result_dict['best_model']
            df_list.append(df)

        result = pd.concat(df_list, axis=0, ignore_index=True)
        
    elif run_type == 'all_best':
        
        fit_result_list = _find_best_model(fit_result_list, model_list)
        
        df_list = list()

        for result_dict in fit_result_list:
            df = pd.DataFrame()
            
            for m in model_list:

                try:
                    fcst = result_dict[m+'_fitted_values'].append(result_dict[m+'_forecast']).values
                    df[m+'_forecast'] = fcst
                    df[m+'_wfa'] = result_dict[m+'_wfa']

                except Exception as e:
                    df[m+'_forecast'] = 0
                    df[m+'_wfa'] = -1
                    print(str(e))

            df['ts_id'] = result_dict['ts_id']
            df['best_model'] = result_dict['best_model']
            df_list.append(df)

        result = pd.concat(df_list, axis=0, ignore_index=True)
                
        
    else:
        df_list = list()
        
        for result_dict in fit_result_list:
            df = pd.DataFrame()

            for m in model_list:

                try:
                    fcst = result_dict[m+'_fitted_values'].append(result_dict[m+'_forecast']).values
                    df[m+'_forecast'] = fcst

                except Exception as e:
                    df[m+'_forecast'] = 0
                    print(str(e))

            df['ts_id'] = result_dict['ts_id']
            df_list.append(df)
        
        result = pd.concat(df_list, axis=0, ignore_index=True) 
    
    return result


def _find_best_model(fit_result_list, model_list):
    
    for result_dict in fit_result_list:
        model_wfa_dict = dict()
        
        for m in model_list:
            model_wfa_dict[m] = result_dict[m+'_wfa']
            
        result_dict['best_model'] = [k for k,v in model_wfa_dict.items() if v == max(model_wfa_dict.values())][0]
    
    return fit_result_list


# not in use
def _transform_dataframe_to_dict(raw_fact, gbkey):
    
    data_param_list = list()
    
    if gbkey is None:
        
        data_param_list.append({'ts_id':1, 'df':raw_fact})
    
    else:
        for k,v in raw_fact.groupby(gbkey):
            data_param_list.append({'ts_id':k, 'df':v})
    
    return data_param_list


