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
    
    
    raw_fact, param_config = _pre_process_user_inputs(
                                                            raw_fact,
                                                            gbkey,
                                                            ds_column, 
                                                            freq, 
                                                            fcst_length, 
                                                            run_type, 
                                                            holdout_length, 
                                                            model_list
                                                    )
    
    fit_result_list = compose.model_fit(raw_fact, model_params, param_config, gbkey)
    
    result = compose.transform_dict_to_df(fit_result_list, model_list)
    
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
    
    param_config['FREQ'] = freq
    param_config['FORECAST_LEN'] = fcst_length
    param_config['HOLDOUT_LEN'] = holdout_length
    param_config['MODEL_LIST'] = model_list
    
    
    if ds_column is None:
        raw_fact['date_stamp'] = pd.date_range(end=datetime.datetime.now(), periods=len(raw_fact), freq='D')
        
    else:
        raw_fact.rename(columns={ds_column: 'date_stamp'}, inplace=True)
    
    
    return raw_fact, param_config
  



