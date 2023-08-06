import neads as nd
import pandas as pd
import matplotlib.pyplot as plt

# Download a list of companies
table = pd.read_html('https://en.wikipedia.org/wiki/S%26P_100')
company_list_as_series = table[2]['Symbol']
company_list_as_tuple = tuple(company_list_as_series)

loader = nd.LoaderRecord(
    'yahoo_loader',
    [{'company_list': company_list_as_tuple,
      'start': '2007-1-1',
      'end': '2009-12-31'}],
    version=0
)

preprocessor = nd.PreprocessorRecord(
    'log_return_preprocessor',
    [{}],
    version=0
)

evolver = nd.EvolverRecord(
    'fix_window_length_evolver',
    [{'length': 60, 'shift': 15}],
    version=0
)

builder_a = nd.BuilderRecord(
    'pearson_correlation_builder',
    [{}],
    version=0
)

builder_b = nd.BuilderRecord(
    'mutual_information_builder',
    [{'normalize': True}],
    version=0
)

filter_ = nd.FilterRecord(
    'planar_maximally_filtered_graph',
    [{}],
    version=0
)

analyzer_a = nd.AnalyzerRecord(
    'average_clustering_coefficient_analyzer',
    [{}],
    version=0
)

analyzer_b = nd.AnalyzerRecord(
    'average_path_length_analyzer',
    [{}],
    version=0
)


def fin_method_1_get_builder_name(data):
    plugin_name = data[0][0].components[4].name
    if plugin_name == 'pearson_correlation_builder':
        return 'Pearson'
    elif plugin_name == 'mutual_information_builder':
        return 'MI'
    else:
        raise NotImplementedError()


def fin_method_1(data):
    values = [
        d['data']
        for _, d in
        sorted(data, key=lambda x: x[0].components[3].params['interval'])
    ]
    name = fin_method_1_get_builder_name(data)
    return {name: values}


def does_contain_plugin(ddf, plugin_name):
    return any(
        c.name == plugin_name for c in ddf.components
    )


def fin_method_2_get_title(data):
    ddf = data[0][0]
    if does_contain_plugin(ddf, 'average_path_length_analyzer'):
        return 'Average path length'
    elif does_contain_plugin(ddf,
                             'average_clustering_coefficient_analyzer'):
        return 'Average clustering coefficient'


def fin_method_2(data):
    d = {**data[0][1], **data[1][1]}
    for method in sorted(d):
        plt.plot(d[method], label=method)
    plt.legend(loc='upper left')
    plt.title(fin_method_2_get_title(data))
    plt.show()


finalizer_1 = nd.FinalizerRecord(
    'finalizer_1',
    [{}],
    version=0,
    method=fin_method_1,
    merge_rules=[nd.NonIndividualReferenceRule(nd.PluginType.EXTRACTOR)],
    take_rules=[nd.NonIndividualReferenceRule(nd.PluginType.ANALYZER)]
)

finalizer_2 = nd.FinalizerRecord(
    'finalizer_2',
    [{}],
    version=0,
    method=fin_method_2,
    merge_rules=[nd.NonIndividualReferenceRule(nd.PluginType.BUILDER)],
    take_rules=[nd.IndividualReferenceRule(finalizer_1)]
)

cfg = nd.Configuration(
    nd.Loading(loader),
    nd.Preprocessing(preprocessor),
    nd.Evolution(evolver),
    nd.Building(builder_a, builder_b),
    nd.WeightedEditing(),
    nd.Filtering(filter_),
    nd.UnweightedEditing(),
    nd.Analyzing(analyzer_a, analyzer_b),
    nd.Finalizing(finalizer_1, finalizer_2)
)
