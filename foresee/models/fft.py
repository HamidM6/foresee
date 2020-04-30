"""
fast fourier transform
"""

import numpy
import pandas

# local module
import models_util


def reconstruct_signal(
                         n_periods,
                         forecast_len,
                         fft_model,
                         ft_sample_frequencies,
                         fft_terms_for_reconstruction,
                         linear_trend
                      ):
    """

    :param n_periods:
    :param fft_model:
    :param ft_sample_frequencies:
    :param fft_terms_for_reconstruction:
    :param linear_trend:
    :return:
    """
    
    pi = numpy.pi
    t = numpy.arange(0, n_periods+forecast_len)
    restored_sig = numpy.zeros(t.size)
    for i in fft_terms_for_reconstruction:
        ampli = numpy.absolute(fft_model[i]) / n_periods
        phase = numpy.angle(
                             fft_model[i],
                             deg = False
                           )
        restored_sig += ampli * numpy.cos(2 * pi * ft_sample_frequencies[i] * t + phase)
    return restored_sig + linear_trend[0] * t


def fft_fit_forecast(ts, fcst_len, n_harmonics):
    
    ts_len = len(ts)
    
    try:
        t = numpy.arange(0, ts_len)
        linear_trend = numpy.polyfit(t, ts, 1)
        training_endog_detrend = ts - linear_trend[0] * t
        fft_model = numpy.fft.fft(training_endog_detrend)
        indexes = list(range(ts_len))
        
        # sort by amplitude
        indexes.sort(
                        key = lambda i: numpy.absolute(fft_model[i]) / ts_len,
                        reverse = True
                    )
        fft_terms_for_reconstruction = indexes[:1 + n_harmonics * 2]
        ft_sample_frequencies = numpy.fft.fftfreq(
                                                    n = ts_len,
                                                    d = 1
                                                 )
        
        fft_fit_forecast = reconstruct_signal(
                                                 n_periods = ts_len,
                                                 forecast_len = fcst_len,
                                                 fft_model = fft_model,
                                                 ft_sample_frequencies = ft_sample_frequencies,
                                                 fft_terms_for_reconstruction = fft_terms_for_reconstruction,
                                                 linear_trend = linear_trend
                                              )
        
        fft_fit_forecast = pandas.Series(fft_fit_forecast).clip(lower=0)
        
        
        fft_fittedvalues = fft_fit_forecast[:-(fcst_len)]
        
        fft_forecast = fft_fit_forecast[-(fcst_len):]
        
        err = None
        
        
    except Exception as e:
        fft_fittedvalues = None
        fft_forecast = None
        err = str(e)
        
    return fft_fittedvalues, fft_forecast, err


def fit_fft(data_dict, freq, fcst_len, model_params, run_type, epsilon):
    
    model = 'fft'
    fft_params = model_params[model]
    n_harmonics = 5
    
    complete_fact = data_dict['complete_fact']
    fft_wfa = None
    
    fft_fitted_values, fft_forecast, err = fft_fit_forecast(
                                                        ts = complete_fact['y'],
                                                        fcst_len = fcst_len,
                                                        n_harmonics = n_harmonics,

                                                    )
    
    
    if run_type in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        fitted_values, forecast, err = fft_fit_forecast(
                                                            ts = train_fact['y'],
                                                            fcst_len = len(test_fact),
                                                            n_harmonics = n_harmonics,
                                                        )
        
        if err is None:
            fft_wfa = models_util.compute_wfa(
                                                    y = test_fact['y'].values,
                                                    yhat = forecast.values,
                                                    epsilon = epsilon,
                                            )
            fft_fitted_values = fitted_values.append(forecast)
            
        else:
            fft_wfa = -1
            
    return fft_fitted_values, fft_forecast, fft_wfa, err
