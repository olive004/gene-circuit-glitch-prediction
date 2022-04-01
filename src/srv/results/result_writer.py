

from src.srv.results.metrics.analytics import Analytics
from src.utils.misc.string_handling import make_time_str


class Result():
    def __init__(self, name, data, category, vis_func, **vis_kwargs) -> None:
        self.name = name
        self.data = data
        self.category = category
        self.vis_func = vis_func
        self.vis_kwargs = vis_kwargs

        self.metrics = []
        self.analytics = Analytics(data, category)
        if category == 'time_series':
            from src.srv.results.metrics.plotting import Timeseries
            self.metrics = Timeseries(data).generate_analytics()


class ResultWriter():
    def __init__(self) -> None:
        self.results = {}

    def add_result(self, result_data, category, vis_func, name, **vis_kwargs):
        """ category: 'time_series', 'graph' """
        name = f'Result_{len(self.results.keys())}' if not name else name
        result_entry = Result(name, result_data, category,
                              vis_func, **vis_kwargs)
        self.results[name] = result_entry

    def get_result(self, key):
        return self.results.get(key, None)

    def make_report(self, keys, source: dict, new_report: bool):
        filename = 'report.txt'
        if new_report:
            filename = filename[:-4] + '_' + make_time_str() + '.txt'
        with open(filename, 'w') as fn:
            for writeable in keys:
                fn.write(f'{writeable}: \n' +
                         str(source.get(writeable, '')) + '\n')

    def write_metrics(self, result: Result, new_report=False):
        metrics = result.metrics
        result.vis_kwargs['save_name'] = f'{result.name}_first_derivative'
        if 'first_derivative' in metrics.keys():
            result.vis_func(metrics['first_derivative'],
                            new_vis=new_report,
                            **result.vis_kwargs)
        writeables = ['steady_state', 'fold_change']
        self.make_report(writeables, metrics, new_report)

    def write_all(self, new_report=False):

        for name, result in self.results.items():
            result.vis_func(
                result.data, new_vis=new_report, **result.vis_kwargs)
            self.write_metrics(result, new_report=new_report)
