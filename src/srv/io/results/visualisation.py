import networkx as nx
import numpy as np
import logging
from src.utils.misc.string_handling import add_outtype, make_time_str
from pyvis.network import Network


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NetworkCustom(Network):
    """ This has since been merged into Networkx officially. """

    def from_nx(self, nx_graph, node_size_transf=(lambda x: x), edge_weight_transf=(lambda x: x),
                default_node_size=10, default_edge_weight=1, show_edge_weights=False,
                use_weighted_opacity=True, invert_opacity=True):
        """
        Overriding default pyvis Network() function to allow show_edge_weights
        """
        assert(isinstance(nx_graph, nx.Graph))
        edges = nx_graph.edges(data=True)
        nodes = nx_graph.nodes(data=True)

        edge_weights = [
            w for (u, v, w) in nx_graph.edges.data('weight', default=0)]
        if np.all(edge_weights == 0) or edge_weights == []:
            edge_w_range = (0, 0)
        else:
            edge_w_range = (np.min(edge_weights), np.max(edge_weights))
        opacity_range = (0, 1)
        if invert_opacity:
            opacity_range = (1, 0)

        if len(edges) > 0:
            for e in edges:
                if 'size' not in nodes[e[0]].keys():
                    nodes[e[0]]['size'] = default_node_size
                nodes[e[0]]['size'] = int(
                    node_size_transf(nodes[e[0]]['size']))
                if 'size' not in nodes[e[1]].keys():
                    nodes[e[1]]['size'] = default_node_size
                nodes[e[1]]['size'] = int(
                    node_size_transf(nodes[e[1]]['size']))
                self.add_node(e[0], **nodes[e[0]])
                self.add_node(e[1], **nodes[e[1]])

                if 'weight' not in e[2].keys():
                    e[2]['weight'] = default_edge_weight
                e[2]['weight'] = edge_weight_transf(e[2]['weight'])
                if show_edge_weights:
                    # These are parameters for pyvis Network() not native to Networkx.
                    # See https://rdrr.io/cran/visNetwork/man/visEdges.html
                    # for edge parameters options.
                    e[2]["label"] = e[2]["weight"]
                if use_weighted_opacity:
                    squashed_w = np.interp(
                        e[2]['weight'], edge_w_range, opacity_range)
                    e[2]["value"] = 1
                    e[2]["color"] = {}
                    e[2]["font"] = {}
                    e[2]["color"]["opacity"] = edge_weight_transf(squashed_w)
                    e[2]["font"] = 5
                self.add_edge(e[0], e[1], **e[2])

        for node in nx.isolates(nx_graph):
            if 'size' not in nodes[node].keys():
                nodes[node]['size'] = default_node_size
            self.add_node(node, **nodes[node])


def visualise_graph_pyvis(graph: nx.DiGraph,
                          out_path: str,
                          new_vis=False):
    import webbrowser
    import os

    out_type = 'html'

    if new_vis:
        out_path = f'{out_path}_{make_time_str()}'
    out_path = add_outtype(out_path, out_type)

    interactive_graph = NetworkCustom(
        height=800, width=800, directed=True, notebook=True)
    interactive_graph.from_nx(graph, edge_weight_transf=lambda x: round(x, 4))
    interactive_graph.inherit_edge_colors(True)
    interactive_graph.set_edge_smooth('dynamic')
    interactive_graph.show(out_path)

    web_filename = 'file:///' + os.getcwd() + '/' + out_path
    webbrowser.open(web_filename, new=1, autoraise=True)


def visualise_graph_pyplot(graph: nx.DiGraph):
    import matplotlib.pyplot as plt
    ax1 = plt.subplot(111)
    nx.draw(graph)
    plt.show()
    raise NotImplementedError


class VisODE():
    def __init__(self) -> None:
        pass

    def plot(self, data, y=None, legend_keys=None, new_vis=False, out_path='test_plot') -> None:
        from src.utils.misc.string_handling import make_time_str
        from matplotlib import pyplot as plt
        timestamp = '' if not(new_vis) else '_' + make_time_str()
        filename = f'{out_path}{timestamp}.png'
        plt.figure()
        if y is not None:
            plt.plot(data, y)
        else:
            plt.plot(data)
        if legend_keys:
            plt.legend(legend_keys)
        plt.savefig(filename)
        plt.close()