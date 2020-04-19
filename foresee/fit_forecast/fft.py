"""
fast fourier transform
"""

import numpy
import pandas

def fit_fft(data_param_dict):
    
    model = 'fft'
    try:
        
        if time_grain == 'week':
            n_harmonics = 20
        elif time_grain == 'month':
            n_harmonics = 8
            
        t = numpy.arange(0, input_length)
        linear_trend = numpy.polyfit(t, input_endog, 1)
        training_endog_detrend = input_endog - linear_trend[0] * t
        fft_model = numpy.fft.fft(training_endog_detrend)
        indexes = list(range(input_length))
        
        # sort by amplitude
        indexes.sort(
                        key = lambda i: numpy.absolute(fft_model[i]) / input_length,
                        reverse = True
                    )
        fft_terms_for_reconstruction = indexes[:1 + n_harmonics * 2]
        ft_sample_frequencies = numpy.fft.fftfreq(
                                                    n = input_length,
                                                    d = 1
                                                 )
        
        fft_fit_forecast = reconstruct_signal(
                                                 n_periods = input_length,
                                                 forecast_length = forecast_length,
                                                 fft_model = fft_model,
                                                 ft_sample_frequencies = ft_sample_frequencies,
                                                 fft_terms_for_reconstruction = fft_terms_for_reconstruction,
                                                 linear_trend = linear_trend
                                              )
        
        fft_fit_forecast = pandas.Series(fft_fit_forecast).clip(lower=0)
        
        
        fft_fittedvalues = fft_fit_forecast[:-(forecast_length)]
        
        fft_forecast = fft_fit_forecast[-(forecast_length):]
        
        err = None
        
        
    except Exception as e:
        fft_model = None
        fft_fittedvalues = None
        fft_forecast = None
        err = str(e)
        
    return fft_model, fft_fittedvalues, fft_forecast, err
        
def reconstruct_signal(
                         n_periods,
                         forecast_length,
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
    t = numpy.arange(0, n_periods+forecast_length)
    restored_sig = numpy.zeros(t.size)
    for i in fft_terms_for_reconstruction:
        ampli = numpy.absolute(fft_model[i]) / n_periods   # amplitude
        phase = numpy.angle(
                             fft_model[i],
                             deg = False
                           )                       # phase in radians
        restored_sig += ampli * numpy.cos(2 * pi * ft_sample_frequencies[i] * t + phase)
    return restored_sig + linear_trend[0] * t
