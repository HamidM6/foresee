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
import json
import matplotlib.pyplot as plt

import foresee.utils
import foresee.compose

root = 'C:\\Users\\abc_h\\Desktop\\github\\foresee'
os.chdir(root)

# default model params 
model_params = foresee.utils.read_json(root, 'model_params.json')

# default model list
# user can remove models from this list

param_config = foresee.utils.read_json(root, 'param_config.json')

"""
TODO: prompt user to accept default or set values
"""
model_list = param_config['model_list']
freq = param_config['freq']
forecast_len = param_config['forecast_len']

# e.g. remove prophet from this list

param_config['model_list'] = [x for x in param_config['model_list'] if x != 'prophet']
param_config['model_list']

# sample ts to test functions

x = np.linspace(0, 200, 40)
ts = 1 + np.sin(x)
plt.plot(ts)

ts_id = 1

ts_fact = {
                    'ts_id': ts_id,
                    'ts': ts,
                }

ts_result = foresee.compose.model_fit(ts_fact, model_params, param_config)


for k,v in ts_result.items():
    err_keys = [x for x in list(v) if 'err' in x]
    for err in err_keys:
        print(v[err])







  



