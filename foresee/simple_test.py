"""
test script at dev stage
"""

import warnings
warnings.filterwarnings('ignore')

import os
os.chdir('C:\\Users\\abc_h\\Desktop\\github\\foresee')

# to run in parallel add current directory to path
import sys
sys.path.append(os.getcwd())

from foresee.scripts.main import prepare_fit_report
from foresee.scripts.utils import read_csv

# sample time-series dataframe with column name 'Close'

ts_df = read_csv('basic_time_series_data.csv')
ts_df.head()

# available forecasting models
model_list = ['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax']

result, _ = prepare_fit_report(ts_df, model_list=model_list)


