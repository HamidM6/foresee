"""
Prophet: facebook's time series forecasting platform.
"""

from fbprophet import Prophet
import pandas as pd

import os

class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

            
            
def fit_prophet(df, freq, forecast_len, model_params):
    
    model = 'prophet'
    prophet_params = model_params[model]
    
    df = df[['date_stamp','y']].reset_index(drop=True)
    df.columns = ['ds', 'y']
        
    try:
        
        prophet_model = Prophet()
        
        #with suppress_stdout_stderr():
        prophet_model.fit(df)
            
        future = prophet_model.make_future_dataframe(periods=forecast_len, freq=freq, include_history=True)
        
        prophet_model_predictions = prophet_model.predict(future)['yhat']
        
        prophet_fittedvalues = prophet_model_predictions.head(len(df))                
        
        prophet_forecast = prophet_model_predictions.tail(forecast_len)
        
        err = None
        
    except Exception as e:
        
        prophet_model = None
        prophet_fittedvalues = None
        prophet_forecast = None
        err = str(e)
        
    return prophet_model, prophet_fittedvalues, prophet_forecast, err

