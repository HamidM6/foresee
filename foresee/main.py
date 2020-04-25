# -*- coding: utf-8 -*-
"""
TODO: provide description
"""

"""
project plan

1) provide functionality to upload user data

2) provide control over model params

3) provide control over stat model type

4) provide control over model/models output

"""
"""
initial support for user data
pandas dataframe with datestamp and time series value columns

df.columns = ['ds', 'y']

type of models:
    
    statsmodels ---> sarimax
    statsmodels ---> holtwinters
    fbprophet   ---> prophet
    

"""

import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

import utils
import compose

root = os.path.dirname(os.getcwd())
# os.chdir(root)

# default model params 
model_params = utils.read_json(root, 'model_params.json')

# default model list
# user can remove models from this list

param_config = utils.read_json(root, 'param_config.json')


"""
TODO: prompt user to accept default or set values
"""

'''
model_list = param_config['model_list']
freq = param_config['freq']
forecast_len = param_config['forecast_len']

e.g. remove prophet from this list

param_config['model_list'] = [x for x in param_config['model_list'] if x != 'prophet']
param_config['model_list']

sample ts to test functions

x = np.linspace(0, 200, 40)
ts = 1 + np.sin(x)
plt.plot(ts)

ts_id = 1

ts_fact = {
                    'ts_id': ts_id,
                    'ts': ts,
                }
ts_result = compose.model_fit(ts_fact, model_params, param_config)

'''


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
    
    return result


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
  



