import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import pandas as pd
from IPython.display import display

PLUGIN_VERSION = 0

TRUE_COL = {
    0: '#80ff00',
    1: '#ff3030'
}
FALSE_COL = {
    0: '#a0a020',
    1: '#ff1080'
}


def fin_2_method(data):
    graph = data[0][1]['data']  # again quite a bad coding style
    analyzers_data = [data[idx][1]['data'] for idx in range(1, len(data))]

    _plot_networks(graph, analyzers_data)
    _plot_evaluation(analyzers_data)


def _plot_networks(graph, analyzers_data):
    num_plots = len(analyzers_data)
    fig, axs = plt.subplots(num_plots, constrained_layout=True,
                            figsize=(6, 4*num_plots))
    for idx in range(num_plots):
        ax = axs[idx]
        a_data = analyzers_data[idx]

        ax.set_title(a_data['title'])
        nx.draw(
            graph,
            pos=nx.spring_layout(graph, seed=21),
            with_labels=True,
            node_color=_generate_colors(graph, a_data['clustering']),
            ax=ax,
        )


def _generate_colors(graph, pred):
    colors = []
    for node, attr in graph.nodes(data=True):
        predicted_cluster = pred[node]
        if predicted_cluster == attr['club']:
            colors.append(TRUE_COL[predicted_cluster])
        else:
            colors.append(FALSE_COL[predicted_cluster])
    return colors


def _plot_evaluation(analyzers_data):
    col_names = _prepare_column_names(analyzers_data[0],
                                      without='clustering')
    d = defaultdict(list)
    for name in col_names:
        for data in analyzers_data:
            d[name].append(data[name])

    df = pd.DataFrame.from_dict(d)
    display(df)


def _prepare_column_names(data, *, without=None):
    columns = list(data.keys())
    if without:
        columns.remove(without)
    return columns
