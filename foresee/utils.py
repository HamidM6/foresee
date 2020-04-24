# -*- coding: utf-8 -*-
"""
local utility functions 
"""

import os
import json
import pandas as pd
import numpy as np

def read_json(file_path, file_name):
    
    json_file = os.path.join(file_path + '\\foresee\\params\\' + file_name)
    
    json_string = open(json_file).read()
    
    return json.loads(json_string.replace('\n', ' ').replace('\t', ' '))


def read_csv(file_path, file_name):
    
    csv_file = os.path.join(file_path + '\\foresee\\data\\' + file_name)
    
    return pd.read_csv(csv_file)




