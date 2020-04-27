"""
Holt-Winters
"""

from statsmodels.tsa.holtwinters import ExponentialSmoothing 

def fit_holt_winters(df, freq, forecast_len, model_params):
    
    model = 'holt_winters'
    hw_params = model_params[model]
    
    ts = df['y']
    
    try:                           
        
        hw_model = ExponentialSmoothing(
                                            endog = ts,
                                            trend = 'add',
                                            damped = True,
                                            seasonal = 'add',
                                            seasonal_periods = freq
                                          ).fit(
                                                optimized = True
                                               )

        hw_fittedvalues = hw_model.fittedvalues    

        hw_forecast = hw_model.predict(
                                            start = len(ts),
                                            end =   len(ts) + forecast_len - 1
                                        )
        err = None
        
    except Exception as e:
        
        hw_model = None
        hw_fittedvalues = None
        hw_forecast = None
        err = str(e)
        
    return hw_model, hw_fittedvalues, hw_forecast, err