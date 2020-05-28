import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stat
import SimPy.Plots.FigSupport as Fig
import SimPy.RandomVariantGenerators as RVGs


COLOR_CONTINUOUS_FIT = 'r'
COLOR_DISCRETE_FIT = 'r'
MIN_PROP = 0.001
MAX_PROB = 0.999
MAX_PROB_DISCRETE = 0.999999


def find_bins(data, bin_width):
    # find bins
    if bin_width is None:
        bins = 'auto'
    else:
        bins = np.arange(min(data), max(data) + bin_width, bin_width)
    return bins


def add_hist(ax, data, bin_width):
    ax.hist(data, density=True, bins=find_bins(data, bin_width),
            edgecolor='black', alpha=0.5, label='Data')


def add_dist(ax, dist, label):
    x_values = np.linspace(dist.ppf(MIN_PROP),
                           dist.ppf(MAX_PROB), 200)
    ax.plot(x_values, dist.pdf(x_values), color=COLOR_CONTINUOUS_FIT, lw=2, label=label)


def format_fig(ax, title, x_label):
    ax.set_title(title)
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0%}'))
    ax.set_xlabel(x_label)
    ax.set_ylabel("Frequency")


def finish_figure(data, ax, bin_width, title, x_label, filename):

    if data is not None:
        add_hist(ax, data, bin_width)

    # format axis
    format_fig(ax, title, x_label)
    ax.legend()

    Fig.output_figure(plt=plt, filename=filename)


def plot_beta_fit(data, fit_results, title=None, x_label=None,
                  fig_size=(6, 5), bin_width=None, filename=None):
    """
    :param data: (numpy.array) observations
    :param fit_results: dictionary with keys "a", "b", "loc", "scale"
    :param title: title of the figure
    :param x_label: label to show on the x-axis of the histogram
    :param fig_size: int, specify the figure size
    :param bin_width: bin width
    :param filename: filename to save the figure as
    """

    # plot histogram
    fig, ax = plt.subplots(1, 1, figsize=fig_size)

    # build the beta distribution
    dist = stat.beta(fit_results['a'], fit_results['b'], fit_results['loc'], fit_results['scale'])

    # plot the distribution
    add_dist(ax, dist, label='Beta')

    finish_figure(data=data, ax=ax, bin_width=bin_width,
                  title=title, x_label=x_label, filename=filename)


def plot_beta_binomial_fit(data, fit_results, title=None, x_label=None,
                           fig_size=(6, 5), bin_width=1, filename=None):
    """
    :param data: (numpy.array) observations
    :param fit_results: dictionary with keys "a", "b", "n", and "loc"
    :param title: title of the figure
    :param x_label: label to show on the x-axis of the histogram
    :param fig_size: int, specify the figure size
    :param bin_width: bin width
    :param filename: filename to save the figure as
    """

    # plot histogram
    fig, ax = plt.subplots(1, 1, figsize=fig_size)

    # plot the estimated distribution
    # calculate PMF for each data point using newly estimated parameters
    x_values = np.arange(0, fit_results['n'], step=1)
    pmf = np.zeros(len(x_values))
    for i in x_values:
        pmf[int(i)] = np.exp(RVGs.BetaBinomial.get_ln_pmf(a=fit_results['a'],
                                                          b=fit_results['b'],
                                                          n=fit_results['n'],
                                                          k=i))

    pmf = np.append([0], pmf[:-1])

    # plot PMF
    ax.step(x_values, pmf, color=COLOR_DISCRETE_FIT, lw=2, label='Beta-Binomial')

    if data is not None:
        add_hist(ax, data, bin_width=bin_width)

    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0%}'))
    ax.set_xlabel(x_label)
    ax.set_ylabel("Frequency")
    ax.legend()
    plt.show()

