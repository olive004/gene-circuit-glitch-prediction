from functools import partial
import numpy as np
from scipy import integrate

from src.utils.misc.decorators import time_it
from src.utils.misc.numerical import zero_out_negs
from src.utils.signal.inputs import Signal
from src.srv.parameter_prediction.simulator import InteractionSimulator
from src.utils.system_definition.agnostic_system.modelling import Deterministic


class SystemManager():

    def __init__(self, system=None) -> None:
        self.system = system


class CircuitModeller():

    def __init__(self) -> None:
        pass

    def init_circuit(self):
        self.compute_interaction_strengths()
        self.find_steady_states()

    def get_modelling_func(self, modeller):
        return partial(modeller.dxdt_RNA, interactions=self.species.interactions,
                       creation_rates=self.species.creation_rates,
                       degradation_rates=self.species.degradation_rates,
                       num_samples=self.species.data.size
                       )

    @time_it
    def compute_interaction_strengths(self):
        interactions = self.run_interaction_simulator(self.species.data.data)
        self.species.interactions = interactions.matrix

    def run_interaction_simulator(self, data):
        simulator = InteractionSimulator(
            self.simulator_args, self.simulator_choice)
        return simulator.run(data)

    def find_steady_states(self):
        modeller_steady_state = Deterministic(
            max_time=50, time_step=1)

        self.species.copynumbers = self.compute_steady_states(modeller_steady_state,
                                                              self.species.copynumbers,
                                                              use_solver='ivp')

        self.result_writer.add_result(self.species.copynumbers,
                                      name='steady_state',
                                      category='time_series',
                                      vis_func=modeller_steady_state.plot,
                                      **{'legend_keys': list(self.species.data.sample_names),
                                         'save_name': 'steady_state_plot'})
        steady_state_metrics = self.result_writer.get_result(
            key='steady_state').metrics
        self.species.steady_state_copynums = steady_state_metrics['steady_state']['steady_states']

    def compute_steady_states(self, modeller, all_copynumbers,
                              use_solver='naive'):
        if use_solver == 'naive':
            self.model_circuit(modeller, all_copynumbers)
        elif use_solver == 'ivp':
            y0 = all_copynumbers[:, -1]
            steady_state_result = integrate.solve_ivp(self.get_modelling_func(modeller),
                                                      (0, modeller.max_time),
                                                      y0=y0)
            if not steady_state_result.success:
                raise ValueError(
                    'Steady state could not be found through solve_ivp.')
            all_copynumbers = steady_state_result.y
        return all_copynumbers

    def model_circuit(self, modeller, copynumbers,
                      signal=None, signal_idx=None):
        modelling_func = self.get_modelling_func(modeller)
        modelling_func = partial(modelling_func, t=None)
        current_copynumbers = copynumbers[:, -1].flatten()
        copynumbers = np.concatenate((copynumbers, np.zeros(
            (self.species.data.size, modeller.max_time-1))
        ), axis=1)
        if signal is not None:
            copynumbers[signal_idx, :] = signal

        copynumbers = self.iterate_modelling_func(copynumbers, current_copynumbers, modelling_func,
                                                  max_time=modeller.max_time, time_step=modeller.time_step,
                                                  signal=signal, signal_idx=signal_idx)
        return copynumbers

    def iterate_modelling_func(self, copynumbers, init_copynumbers,
                               modelling_func, max_time, time_step,
                               signal=None, signal_idx=None):
        current_copynumbers = init_copynumbers
        for tstep in range(0, max_time-1):
            dxdt = modelling_func(
                copynumbers=copynumbers[:, tstep]) * time_step

            current_copynumbers = np.add(dxdt, current_copynumbers).flatten()

            if signal is not None:
                current_copynumbers[signal_idx] = signal[tstep]
            current_copynumbers = zero_out_negs(current_copynumbers)
            copynumbers[:, tstep +
                        1] = current_copynumbers
        return copynumbers

    def simulate_signal(self, signal: Signal = None):
        if signal is None:
            return
        signal_modeller = Deterministic(
            max_time=signal.total_time, time_step=1
        )
        new_copynumbers = self.model_circuit(signal_modeller,
                                             self.species.steady_state_copynums,
                                             signal=signal.real_signal,
                                             signal_idx=signal.identities_idx)

        self.species.copynumbers = np.concatenate(
            (self.species.copynumbers, new_copynumbers[:, 1:]), axis=1)
        self.result_writer.add_result(new_copynumbers,
                                      name='signal',
                                      category='time_series',
                                      vis_func=signal_modeller.plot,
                                      **{'legend_keys': list(self.species.data.sample_names),
                                         'save_name': 'signal_plot'})