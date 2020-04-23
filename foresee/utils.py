# -*- coding: utf-8 -*-
"""
local utility functions 
"""

import os
import json
import pandas as pd

def read_json(file_path, file_name):
    
    json_file = os.path.join(file_path + '\\foresee\\params\\' + file_name)
    
    json_string = open(json_file).read()
    
    return json.loads(json_string.replace('\n', ' ').replace('\t', ' '))


def read_csv(file_path, file_name):
    
    csv_file = os.path.join(file_path + '\\foresee\\params\\' + file_name)
    
    return pd.read_csv(csv_file)

def transform_dict_to_df(fit_results, model_list):
    
    df = pd.DataFrame()
    
    for m in model_list:
        
        try:
            fcst = np.concatenate([fit_results[m+'_fitted_values'], fit_results[m+'_forecast']])
            
            df[m+'_forecast'] = fcst
            
        except:
            df[m+'_forecast'] = 0
    
    
    return df


