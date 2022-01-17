import rpy2.robjects as ro

from pandas import DataFrame
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

ro.r['source']('fit_lmem.R')


def compute_estimates_and_cis(data: DataFrame, formula: str, ci_method: str = 'profile') -> DataFrame:
    """Computes parameter estimates and 95% confidence intervals for a given dataset, model formula and confidence
    interval estimation method using the R function defined in the fit_lmem.R script.

    :param data: dataset to be processed.
    :param formula: linear mixed effects model formula to estimate parameters for.
    :param ci_method: method to use for confidence interval estimation. Defaults to the "profile" method.
    :return: DataFrame containing parameter estimates, 95% confidence intervals and p-values of the estimates.

    """
    lmem_r_function = ro.globalenv['compute_estimates_and_conf_ints']

    with localconverter(ro.default_converter + pandas2ri.converter):
        data_r = ro.conversion.py2rpy(data)

    r_estimates = lmem_r_function(
        data=data_r,
        formula=formula,
        ci_method=ci_method,
    )

    # TODO: There has to be a more elegant way of doing this...
    return DataFrame([
        {
            'Name': 'Intercept',
            'Estimate': round(r_estimates.rx['estimate_intercept'][0][0], 3),
            '95% CI': tuple(map(lambda x: round(x, 3), tuple(r_estimates.rx['conf_int_intercept'][0]))),
            'P-Value': round(r_estimates.rx['estimate_intercept'][0][1], 3),
        },

        {
            'Name': 'Time',
            'Estimate': round(r_estimates.rx['estimate_time'][0][0], 3),
            '95% CI': tuple(map(lambda x: round(x, 3), tuple(r_estimates.rx['conf_int_time'][0]))),
            'P-Value': round(r_estimates.rx['estimate_time'][0][1], 3),
        },
    ])
