import neads as nd
import pandas as pd

# Download a list of companies
table = pd.read_html('https://en.wikipedia.org/wiki/S%26P_100')
company_list = tuple(table[2]['Symbol'])


def _get_cfg(finalizer_name):
    return nd.Configuration(
        nd.Loading(
            nd.LoaderRecord(
                'yahoo_loader',
                [{'company_list': company_list,
                  'start': '2007-1-1',
                  'end': '2009-12-31'}],
                version=0
            )
        ),
        nd.Preprocessing(
            nd.PreprocessorRecord('relative_change_preprocessor', [{}],
                                  version=0)
        ),
        nd.Evolution(),
        nd.Building(nd.BuilderRecord('pearson_correlation_builder', [{}],
                                     version=0)),
        nd.WeightedEditing(),
        nd.Filtering(nd.FilterRecord('weight_threshold_filter',
                                     [{'threshold': 0.65}], version=0)),
        nd.UnweightedEditing(),
        nd.Analyzing(
            nd.AnalyzerRecord('degree_distribution_analyzer', [{}],
                              version=0)),
        nd.Finalizing(
            nd.FinalizerRecord(
                finalizer_name,
                [{}],
                version=0,
                merge_rules=[],
                take_rules=[
                    nd.NonIndividualReferenceRule(nd.PluginType.ANALYZER)
                ]
            )
        )
    )


tutorial_02_cfg_histogram = _get_cfg('bar_plot_finalizer')
tutorial_02_cfg_log_log = _get_cfg('log_log_plot_finalizer')
