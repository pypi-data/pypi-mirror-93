import pandas as pd
from IPython.display import display

names = {
    'node_count_analyzer': 'Nodes',
    'edge_count_analyzer': 'Edges',
    'average_degree_analyzer': 'Average degree',
    'degree_standard_deviation_analyzer': 'Std. of degree',
    'average_clustering_coefficient_analyzer': 'Average clustering '
                                               'coefficient',
    'average_path_length_analyzer': 'Average path length',
    'diameter_analyzer': 'Diameter'
}

idx = {
    'p_1': 1,
    'b': 3,
    'f': 4
}


def get_name(ddf):
    window = ddf.components[idx['p_1']].params['window_length']
    builder = 'Pearson' \
        if ddf.components[idx['b']].name == 'pearson_correlation_builder' \
        else 'MI'
    if ddf.components[idx['f']].name == 'planar_maximally_filtered_graph':
        filter_ = 'PMFG'
    elif ddf.components[idx['f']].name == 'preserving_quotient_filter':
        filter_ = f'quotient' \
                  f' {ddf.components[idx["f"]].params["quotient"]}'
    else:
        filter_ = f'threshold' \
                  f' {ddf.components[idx["f"]].params["threshold"]}'

    name = f'Window: {window}, Builder: {builder}, Filter: {filter_}'
    return name


def tutorial_04_finalizer_method(data):
    sorted_ = [
        next(
            filter(
                lambda pair: pair[0].components[-1].name == a, data
            )
        )
        for a, name in names.items()
    ]  # sorted tuples (ddf, data)
    kv_pairs = {
        name: sorted_[idx][1]['data']  # take the data dict and key 'data'
        for idx, name in enumerate(names.values())
    }
    series = pd.Series(kv_pairs)
    series.name = get_name(data[0][0])
    display(series)
