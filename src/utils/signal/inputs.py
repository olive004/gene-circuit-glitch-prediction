from functools import partial
import numpy as np


class Signal():
    def __init__(self, identities_idx, signal=None,
                 total_time=None,
                 time_interval=1,
                 magnitude=1) -> None:
        self.identities_idx = identities_idx
        self.abstract_signal = signal if signal is not None else [0, 1]
        self.total_time = total_time if total_time else len(
            self.abstract_signal)
        self.magnitude = magnitude
        self.time_interval = time_interval
        self.time_steps = time_interval * total_time
        self.time_dilation_func = partial(np.repeat, repeats=self.time_steps)

    @property
    def abstract_signal(self):
        return self._abstract_signal

    @abstract_signal.setter
    def abstract_signal(self, value):
        self._abstract_signal = value

    @property
    def real_signal(self):
        return self.time_dilation_func(self.abstract_signal) * self.magnitude

    @property
    def time(self):
        return np.arange(0, self.total_time, self.time_interval)

    def show(self, signal_name='input_signal_plot'):
        from src.srv.results.visualisation import VisODE
        VisODE().plot(data=self.time, y=self.real_signal, save_name=signal_name)


class AdaptationTarget(Signal):
    def __init__(self, identities_idx, signal_type='double_exp',
                 signal=None, total_time=None, time_interval=1, magnitude=1) -> None:
        super().__init__(identities_idx, signal, total_time, time_interval, magnitude)

        self.signal_type = signal_type

    @property
    def real_signal(self):
        return self.adapt_pulse(self.time_steps, height=self.magnitude, pulse_type=self.signal_type)

    def adapt_pulse(self, time_points, height, pulse_type):
        ''' Adaptation response curves
        From Shen et al. 2021 https://doi.org/10.1038/s41467-021-23420-5 
        https://github.com/sjx93/rnn_for_gene_network_2020/blob/main/fig1-2_adaptation/target_response_curves.py '''

        def adapt_pulse_double_exp(height) -> np.array:
            # inputs: scalars
            # output: np.array of shape=time_points
            # double exponential response curve
            xs0 = self.time
            y = height*4*(np.exp(-xs0/6) - np.exp(-xs0/3))
            return y

        def adapt_pulse_triangular(height) -> np.array:
            # triangular pulse for the adaptation task
            xs0 = self.time
            y = height * 2 * np.maximum(np.minimum(0.1*xs0, 1-0.1*xs0), 0)
            return y

        if pulse_type == 'double_exp':
            return adapt_pulse_double_exp(height)
        elif pulse_type == 'triangular':
            return adapt_pulse_triangular(height)
        else:
            raise ValueError(f'Could not recognise pulse type {pulse_type}')


class OscillatingSignal(Signal):
    def __init__(self, identities_idx, signal=None, total_time=None, magnitude=1) -> None:
        super().__init__(identities_idx, signal, total_time, magnitude)
