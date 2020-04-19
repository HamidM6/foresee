"""
Holt-Winters
"""

from statsmodels.tsa.holtwinters import ExponentialSmoothing 

def fit_holt_winters(data_param_dict):
    
    model = 'holt_winters'
    
    if time_grain == 'week':
        seasonal_periods = 52
    elif time_grain == 'month':
        seasonal_periods = 12
    
    try:                           
        
        holt_winters_model = ExponentialSmoothing(
                                                    endog = input_endog,
                                                    trend = 'add',
                                                    damped = True,
                                                    seasonal = 'add',
                                                    seasonal_periods = seasonal_periods
                                                  ).fit(
                                                        optimized = True
                                                       )

        holt_winters_fittedvalues = holt_winters_model.fittedvalues.round().clip(lower=0)     

        holt_winters_forecast = holt_winters_model.predict(
                                                                start = input_length,
                                                                end =   input_length + forecast_length - 1
                                                            ).round().clip(lower=0)
        err = None
        
    except Exception as e:
        
        holt_winters_model = None
        holt_winters_fittedvalues = None
        holt_winters_forecast = None
        err = str(e)
        
    return holt_winters_model, holt_winters_fittedvalues, holt_winters_forecast, err