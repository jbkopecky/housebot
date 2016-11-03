import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator


def plot_results(data):
    # Plot results: Train / Test cross plot.
    # data: {title: [y_train_pred, y_train], title:[y_test_pred, y_test]}
    ncols = len(data.keys())
    fig, axes = plt.subplots(nrows=1, ncols=ncols, figsize=(12, 5))
    style = {
            'alpha': 0.8,
            's': 20.,
            'lw': 0.,
            }
    titles = sorted(data.keys())
    for i, key in enumerate(titles):
        y_pred = data[key][0]
        y_actual = data[key][1]
        ax = axes[i] if len(titles) > 1 else axes
        ax.scatter(y_pred, y_actual, c='grey', **style)
        ax.plot([0., 100000.], [0., 100000.], c='b')
        ax.plot([0., 75000.], [0., 100000.], c='b')
        ax.plot([0., 100000.], [0., 75000.], c='b')
        ax.set_xlabel('Predicted Price per m2')
        ax.set_ylabel('Actual Price per m2')
        ax.set_title(key)
        ax.set_ylim(0., 47000.)
        ax.set_xlim(0., 18000.)
        ax.grid()


def plot_compare_feature_levels(data):
    # [(name, value), (name, value) ....]
    ra = range(len(data))
    plt.barh(ra, [x[1] for x in data], align='center', alpha=0.4)
    plt.yticks(ra, [x[0] for x in data])


def sort_dict_by(dict_to_sort, by=0):
    # 1: sort on values, 0: sort on keys
    return sorted(dict_to_sort.items(), key=operator.itemgetter(by))


def make_xy_data(csv, drop_nan_columns=None):
    data = pd.read_csv(csv, index_col=0)
    n = len(data)

    if drop_nan_columns:
        data = data.dropna(subset=drop_nan_columns)

    print "[Warning] dropped %s samples because of NaN values" % (n-len(data))

    y = np.divide(data[['prix']].astype(float).values.T,
                  data[['surface_m2']].astype(float).values.T
                  )[0]

    x = data.drop(['prix'], axis=1)

    return x, y


def plot_ic_criterion(model, name, color):
    alpha_ = model.alpha_
    alphas_ = model.alphas_
    criterion_ = model.criterion_
    plt.plot(-np.log10(alphas_), criterion_, '--', color=color,
             linewidth=3, label='%s criterion' % name)
    plt.axvline(-np.log10(alpha_), color=color, linewidth=3,
                label='alpha: %s estimate' % name)
    plt.xlabel('-log(alpha)')
    plt.ylabel('criterion')
