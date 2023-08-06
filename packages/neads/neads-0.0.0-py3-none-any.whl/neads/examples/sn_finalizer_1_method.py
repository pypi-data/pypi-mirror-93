from networkx.algorithms.community import modularity
from itertools import chain
from statistics import mean
from sklearn import metrics

PLUGIN_VERSION = 0


def fin_1_method(data):
    ddc, pred_clustering, true_clustering, G = _get_parsed_data(data)
    description = {
        'title': _get_title(ddc),
        'clustering': pred_clustering,
        'accuracy': _compute_accuracy(pred_clustering, true_clustering),
        'modularity': _compute_modularity(pred_clustering, G),
        'mutual_info': _compute_mutual_info(pred_clustering,
                                            true_clustering)
    }
    return {'data': description}


def _get_parsed_data(data):
    # two ddc in data - graph and the predicted clustering

    def get_builder_index():
        def is_editor(ddf):
            # quite bad coding.. relies on prefix of the plugin name
            return ddf.components[-1].name.endswith('editor')

        first_ddf = data[0][0]
        return 0 if is_editor(first_ddf) else 1

    def get_true_clustering():
        _, d = data[get_builder_index()]
        G = d['data']
        return {node: attr['club'] for node, attr in G.nodes(data=True)}

    def get_graph():
        _, d = data[get_builder_index()]
        G = d['data']
        return G

    def get_analyzer_ddc():
        ddf, _ = data[1 - get_builder_index()]
        return ddf.components[-1]

    def get_pred_clustering():
        _, d = data[1 - get_builder_index()]
        clusters = d['data']
        cluster_a, cluster_b = clusters
        cluster_0 = cluster_a if 0 in cluster_a else cluster_b
        return {node: (0 if node in cluster_0 else 1)
                for node in chain(cluster_a, cluster_b)}

    return get_analyzer_ddc(), get_pred_clustering(), \
        get_true_clustering(), get_graph()


def _get_title(ddc):
    return f'{ddc.name} {ddc.params}'


def _compute_accuracy(pred, true):
    return mean(pred[node] == true[node] for node in pred)


def _compute_modularity(pred, G):
    communities = []
    for c in range(2):
        communities.append({node for node in pred if pred[node] == c})
    return modularity(G, communities)


def _compute_mutual_info(pred, true):
    labels_true, labels_pred = [], []
    for node in pred:
        labels_true.append(true[node])
        labels_pred.append(pred[node])
    return metrics.adjusted_mutual_info_score(labels_true, labels_pred)
