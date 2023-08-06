import neads as nd
from neads.examples.sn_finalizer_1_method import fin_1_method
from neads.examples.sn_finalizer_2_method import fin_2_method

loader = nd.LoaderRecord(
    'empty_loader',
    [{}],
    version=0
)

builder = nd.BuilderRecord(
    'networkx_generator_builder',
    [{'name': 'karate_club_graph'}],
    version=0
)


def editor_method(data):
    ddf, d = data
    G = d['data'].copy()
    for node, data in G.nodes(data=True):
        data['club'] = 0 if data['club'] == 'Mr. Hi' else 1
    return {'data': G}


editor = nd.UnweightedEditorRecord(
    'karate_club_cluster_editor',
    [{}],
    version=0,
    method=editor_method
)

analyzer_a = nd.AnalyzerRecord(
    'kernighan_lin_analyzer',
    [
        {'max_iter': 10, 'seed': 0},
        {'max_iter': 10, 'seed': 1}
    ],
    version=0
)

analyzer_b = nd.AnalyzerRecord(
    'fluid_communities_analyzer',
    [
        {'communities_count': 2, 'max_iter': 100, 'seed': 0},
        {'communities_count': 2, 'max_iter': 100, 'seed': 1}
    ],
    version=0
)

analyzer_c = nd.AnalyzerRecord(
    'girvan_newman_analyzer',
    [{'communities_count': 2}],
    version=0
)

finalizer_1 = nd.FinalizerRecord(
    'finalizer_single_clustering',
    [{}],
    version=0,
    method=fin_1_method,
    merge_rules=[],
    take_rules=[nd.NonIndividualReferenceRule(nd.PluginType.ANALYZER),
                nd.IndividualReferenceRule(editor)],
)

finalizer_2 = nd.FinalizerRecord(
    'finalizer_plot_results',
    [{}],
    version=0,
    method=fin_2_method,
    merge_rules=[nd.NonIndividualReferenceRule(nd.PluginType.ANALYZER)],
    take_rules=[nd.IndividualReferenceRule(finalizer_1),
                nd.IndividualReferenceRule(editor)]
)

cfg = nd.Configuration(
    nd.Loading(loader),
    nd.Preprocessing(),
    nd.Evolution(),
    nd.Building(builder),
    nd.WeightedEditing(),
    nd.Filtering(),
    nd.UnweightedEditing(editor),
    nd.Analyzing(analyzer_a, analyzer_b, analyzer_c),
    nd.Finalizing(finalizer_1, finalizer_2)
)