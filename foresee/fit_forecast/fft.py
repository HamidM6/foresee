"""
fast fourier transform
"""

import numpy
import pandas

def fit_fft(df, freq, forecast_len, model_params):
    
    model = 'fft'
    fft_params = model_params[model]
    
    ts = df['y'].values
    
    ts_len = len(ts)
    
    
    try:
        
        n_harmonics = 5
        
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
                                                 forecast_len = forecast_len,
                                                 fft_model = fft_model,
                                                 ft_sample_frequencies = ft_sample_frequencies,
                                                 fft_terms_for_reconstruction = fft_terms_for_reconstruction,
                                                 linear_trend = linear_trend
                                              )
        
        fft_fit_forecast = pandas.Series(fft_fit_forecast).clip(lower=0)
        
        
        fft_fittedvalues = fft_fit_forecast[:-(forecast_len)]
        
        fft_forecast = fft_fit_forecast[-(forecast_len):]
        
        err = None
        
        
    except Exception as e:
        fft_model = None
        fft_fittedvalues = None
        fft_forecast = None
        err = str(e)
        
    return fft_model, fft_fittedvalues, fft_forecast, err
        
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
        ampli = numpy.absolute(fft_model[i]) / n_periods   # amplitude
        phase = numpy.angle(
                             fft_model[i],
                             deg = False
                           )                       # phase in radians
        restored_sig += ampli * numpy.cos(2 * pi * ft_sample_frequencies[i] * t + phase)
    return restored_sig + linear_trend[0] * t
