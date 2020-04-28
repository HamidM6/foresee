"""
exponentially weighted moving average
"""

import numpy as np
import pandas as pd

def fit_ewm(df, freq, forecast_len, model_params):
    
    model = 'ewm_model'
    ewm_params = model_params[model]
    
    ts = df['y']
    
    span = 5
    
    try:
        
        ewm_model = pd.Series(ts).ewm(span=span)
        ewm_fittedvalues = ewm_model.mean()
        
        ewm_forecast = np.empty(forecast_len)
        ewm_forecast.fill(ewm_fittedvalues.iloc[-1])
        ewm_forecast = pd.Series(ewm_forecast)
        err = None

    except Exception as e:
        
        ewm_model = None
        ewm_fittedvalues = None
        ewm_forecast = None
        err = str(e)
        
    return ewm_model, ewm_fittedvalues, ewm_forecast, err