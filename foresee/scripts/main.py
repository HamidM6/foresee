# -*- coding: utf-8 -*-
"""
Joins user input with parameters configuration and stat models configuration
and combines forecast results
"""

import os
import pandas as pd
import numpy as np
import datetime

from foresee.scripts import utils
from foresee.scripts import compose

# default model params
model_params = utils.read_json('model_params.json')

# parameters configuration
param_config = utils.read_json('param_config.json')


def collect_result(
                        raw_fact,
                        endog_colname,
                        gbkey,
                        ds_column, 
                        freq, 
                        fcst_length, 
                        run_type, 
                        holdout_length,
                        model_list,
                        processing_method,
                        tune,
                    ):
    """[summary]

    Parameters
    ----------
    raw_fact : [type]
        [description]
    endog_colname : [type]
        [description]
    gbkey : [type]
        [description]
    ds_column : [type]
        [description]
    freq : [type]
        [description]
    fcst_length : [type]
        [description]
    run_type : [type]
        [description]
    holdout_length : [type]
        [description]
    model_list : [type]
        [description]
    processing_method : [type]
        [description]
    tune : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    
    
    pre_processed_dict, param_config = _pre_process_user_inputs(
                                                                    raw_fact,
                                                                    endog_colname,
                                                                    gbkey,
                                                                    ds_column, 
                                                                    freq, 
                                                                    fcst_length, 
                                                                    run_type, 
                                                                    holdout_length,
                                                                    model_list,
                                                            )
    
    result, fit_result_list = compose.compose_fit(
                                                        pre_processed_dict,
                                                        model_params,
                                                        param_config,
                                                        gbkey,
                                                        run_type,
                                                        processing_method,
                                                        tune,
                                                )
    
    return result, fit_result_list


def _pre_process_user_inputs(
                                    raw_fact,
                                    endog_colname,
                                    gbkey,
                                    ds_column, 
                                    freq, 
                                    fcst_length, 
                                    run_type, 
                                    holdout_length, 
                                    model_list
                            ):
    """[summary]

    Parameters
    ----------
    raw_fact : [type]
        [description]
    endog_colname : [type]
        [description]
    gbkey : [type]
        [description]
    ds_column : [type]
        [description]
    freq : [type]
        [description]
    fcst_length : [type]
        [description]
    run_type : [type]
        [description]
    holdout_length : [type]
        [description]
    model_list : [type]
        [description]

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    ValueError
        [description]
    """    
    
    # next 4-lines can be done better
    
    param_config['FREQ'] = freq
    param_config['FORECAST_LEN'] = fcst_length
    param_config['HOLDOUT_LEN'] = holdout_length
    param_config['MODEL_LIST'] = model_list
    
    # replace endog column name with 'y'
    
    if len(raw_fact.columns) == 1:
        raw_fact.columns = ['y']
    else:
        if endog_colname in raw_fact.columns:
            raw_fact.rename(columns={endog_colname: 'y'}, inplace=True)
        else:
            #TODO: display this error to user
            raise ValueError('time series column name not found!!!')

    
    # add or rename date-time column
    
    if ds_column not in raw_fact.columns:
        raw_fact['date_stamp'] = pd.date_range(end=datetime.datetime.now(), periods=len(raw_fact), freq='D')
        
    else:
        raw_fact.rename(columns={ds_column: 'date_stamp'}, inplace=True)
        raw_fact['date_stamp'] = pd.to_datetime(raw_fact['date_stamp'])
        
    #TODO: if user chose to compare models, then create train-holdout sets
    #TODO: missing data interpolation, needs user input!
    
    pre_processed_dict = dict()    
        
    if run_type in ['best_model', 'all_best']:
        
        if gbkey in raw_fact.columns:
            for k,v in raw_fact.groupby(gbkey):
                train_fact = v.iloc[:-holdout_length]
                test_fact = v.iloc[-holdout_length:]
                v['data_split'] = np.concatenate([np.full(len(train_fact), 'Train'), np.full(len(test_fact), 'Test')])

                pre_processed_dict[k] = {'complete_fact': v, 'train_fact': train_fact, 'test_fact': test_fact}
                
        else:
            train_fact = raw_fact.iloc[:-holdout_length]
            test_fact = raw_fact.iloc[-holdout_length:]
            raw_fact['data_split'] = np.concatenate([np.full(len(train_fact), 'Train'), np.full(len(test_fact), 'Test')])
            
            pre_processed_dict[1] = {'complete_fact': raw_fact, 'train_fact': train_fact, 'test_fact': test_fact}
            
            
    else:
        if gbkey in raw_fact.columns:
            for k,v in raw_fact.groupby(gbkey):
                v['data_split'] = 'Train'
                pre_processed_dict[k] = {'complete_fact': v}
                
        else:
            raw_fact['data_split'] = 'Train'
            pre_processed_dict[1] = {'complete_fact': raw_fact}
            
    
    return pre_processed_dict, param_config
  



