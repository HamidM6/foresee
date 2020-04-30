# -*- coding: utf-8 -*-
"""
combine user input with parameters configuration and stat models configuration
"""

import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

import utils
import compose

# default model params
model_params = utils.read_json('model_params.json')

# parameters configuration
param_config = utils.read_json('param_config.json')


"""
TODO: prompt user to accept default or set values
"""

"""
TODO: provide function documentation
"""

"""
run_type:
    all_models: return the result for all models without comparing out of sample forecast accuracy
    best_model: return the result for model with highest out of sample forecast accuracy
    all_best:   return the result for all models and indicate the model with highest out of sample forecast accuracy
"""

def collect_result(
                        raw_fact,
                        gbkey,
                        ds_column, 
                        freq, 
                        fcst_length, 
                        run_type, 
                        holdout_length, 
                        model_list
                    ):
    
    
    pre_processed_dict, param_config = _pre_process_user_inputs(
                                                            raw_fact,
                                                            gbkey,
                                                            ds_column, 
                                                            freq, 
                                                            fcst_length, 
                                                            run_type, 
                                                            holdout_length, 
                                                            model_list
                                                    )
    
    result, fit_result_list = compose.compose_fit(pre_processed_dict, model_params, param_config, gbkey, run_type)
    
    return result, fit_result_list


def _pre_process_user_inputs(
                                    raw_fact,
                                    gbkey,
                                    ds_column, 
                                    freq, 
                                    fcst_length, 
                                    run_type, 
                                    holdout_length, 
                                    model_list
                            ):
    """
    add or rename date stamp column to input dataframe
    if comparing models results, separate input data to train-test dataframes
    """
    
    # next 4-lines can be done better
    param_config['FREQ'] = freq
    param_config['FORECAST_LEN'] = fcst_length
    param_config['HOLDOUT_LEN'] = holdout_length
    param_config['MODEL_LIST'] = model_list
    
    
    
    if ds_column is None:
        raw_fact['date_stamp'] = pd.date_range(end=datetime.datetime.now(), periods=len(raw_fact), freq='D')
        
    else:
        raw_fact.rename(columns={ds_column: 'date_stamp'}, inplace=True)
        raw_fact['date_stamp'] = pd.to_datetime(raw_fact['date_stamp'])
        
    #TODO: if user chose to compare models, then create train-holdout sets
    #TODO: missing data interpolation, needs user input!
    
    pre_processed_dict = dict()    
        
    if run_type in ['best_model', 'all_best']:
        
        if gbkey is None:
            train_fact = raw_fact.iloc[:-holdout_lenght]
            test_fact = raw_fact.iloc[-holdout_lenght:]
            pre_processed_dict[1] = {'complete_fact': raw_fact, 'train_fact': train_fact, 'test_fact': test_fact}
            
        else:
            for k,v in raw_fact.groupby(gbkey):
                train_fact = v.iloc[:-holdout_length]
                test_fact = v.iloc[-holdout_length:]

                pre_processed_dict[k] = {'complete_fact': v, 'train_fact': train_fact, 'test_fact': test_fact}
            
    else:
        if gbkey is None:
            pre_processed_dict[1] = {'complete_fact': raw_fact}
            
        else:
            for k,v in raw_fact.groupby(gbkey):
                pre_processed_dict[k] = {'complete_fact': v}
    
    return pre_processed_dict, param_config
  



