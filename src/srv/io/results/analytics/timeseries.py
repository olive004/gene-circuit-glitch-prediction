import logging
import numpy as np


class Timeseries():
    def __init__(self, data) -> None:
        self.data = data
        self.num_dtype = np.float32

        self.stability_threshold = 0.01

    def get_steady_state(self):
        """ Last 5% of data considered steady state """
        final_deriv = np.average(
            self.get_derivative()[:, :-2])
        is_steady_state_reached = final_deriv < self.stability_threshold
        steady_states = np.expand_dims(self.data[:, -1], axis=1)
        return {
            "is_steady_state_reached": is_steady_state_reached,
            "steady_states": steady_states,
            "final_deriv": final_deriv
        }

    def fold_change(self):
        division_vector = self.data[:, -1].clip(1)
        division_matrix = np.divide(division_vector, division_vector.T)
        return division_matrix

    def get_derivative(self):
        deriv = np.gradient(self.data)[1]
        return deriv  # get column derivative

    def get_overshoot(self, steady_states):
        return np.max(self.data, axis=1) - steady_states

    def get_precision(self, steady_states, signal_idx):
        starting_states = self.data[:, 0]
        signal_low = np.min(self.data[signal_idx, :])
        signal_high = np.max(self.data[signal_idx, :])
        
        return np.absolute(np.divide(
            (steady_states - starting_states) / starting_states,
            (signal_high - signal_low) / signal_low
        ))

    def get_sensitivity(self, signal_idx):
        starting_states = self.data[:, 0]
        peaks = np.max(self.data, axis=1)
        signal_low = np.min(self.data[signal_idx, :])
        signal_high = np.max(self.data[signal_idx, :])

        return np.absolute(np.divide(
            (peaks - starting_states) / starting_states,
            (signal_high - signal_low) / signal_low
        ))


    def get_response_times(self, steady_states):
        margin_high = 1.05
        margin_low = 0.95
        peak = np.max(self.data)
        has_peak = np.all(peak > steady_states)
        if has_peak:
            post_peak_data = self.data[:, np.argmax(
                self.data < np.max(self.data)):]
            response_time = np.expand_dims(np.argmax(
                post_peak_data < steady_states, axis=1).astype(self.num_dtype), axis=1)
            response_time_high = np.expand_dims(np.argmax(post_peak_data < (
                steady_states * margin_high), axis=1).astype(self.num_dtype), axis=1)
            response_time_low = np.expand_dims(np.argmax(post_peak_data < (
                steady_states * margin_low), axis=1).astype(self.num_dtype), axis=1)
        else:
            post_peak_data = self.data
            response_time = np.expand_dims(np.argmax(
                post_peak_data >= steady_states, axis=1).astype(self.num_dtype), axis=1)
            response_time_high = np.expand_dims(np.argmax(post_peak_data >= (
                steady_states * margin_high), axis=1).astype(self.num_dtype), axis=1)
            response_time_low = np.expand_dims(np.argmax(post_peak_data >= (
                steady_states * margin_low), axis=1).astype(self.num_dtype), axis=1)
        # logging.info(post_peak_data < steady_states)
        # logging.info(post_peak_data >= steady_states)
        # logging.info(np.argmax(post_peak_data >= steady_states, axis=1).astype(self.num_dtype))
        # logging.info(post_peak_data < (steady_states * 1.05))
        # logging.info(post_peak_data < (steady_states * 0.95))
        return response_time, response_time_high, response_time_low

    def get_writeables(self):
        return ['fold_change', 'steady_state', 'response_time', 'response_time_high', 'response_time_low']

    def frequency(self):
        spectrum = np.fft.fft(self.data)/len(self.data)
        spectrum = spectrum[range(int(len(self.data)/2))]
        freq = np.fft.fftfreq(len(spectrum))
        return freq

    def generate_analytics(self):
        analytics = {
            'first_derivative': self.get_derivative(),
            'fold_change': self.fold_change(),
            'steady_state': self.get_steady_state()
        }
        analytics['response_time'], \
            analytics['response_time_high'], \
            analytics['response_time_low'] = self.get_response_times(
            analytics['steady_state']['steady_states'])
        
        analytics['overshoot'] = self.get_overshoot(analytics['steady_state']['steady_states'])
        analytics['precision'] = self.get_precision(analytics['steady_state']['steady_states'])
        analytics['sensitivity'] = self.get_sensitivity(analytics['steady_state']['steady_states'])
        return analytics
