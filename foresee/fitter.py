# -*- coding: utf-8 -*-
"""
fitter class
"""

from fit_forecast.holt_winters import fit_holt_winters
from fit_forecast.sarimax import fit_sarimax
from fit_forecast.ewm import fit_ewm
from fit_forecast.prophet import fit_prophet
from fit_forecast.fft import fit_fft

class fitter:
    
    FIT_MODELS = {
                    'holt_winters':     fit_holt_winters,
                    'sarimax':          fit_sarimax,
                    'ewm_model':        fit_ewm,
                    'prophet':          fit_prophet,
                    'fft':              fit_fft,
                 }
    
    
    def __init__(self, model):
         self.model = model
         
    
    def fit(self, ts, freq, forecast_len, model_params):
        """

        :param data_param_dict: ts values and parameters
        """
        fit_model = self.FIT_MODELS[self.model]
        
        return fit_model(ts, freq, forecast_len, model_params)