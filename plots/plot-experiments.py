import argparse
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_experiment(experiment: str, save_fig: bool = False):
    # Paths to the CSV files
    file_paths = [
        "./{}-results/processed-mprm.csv".format(experiment),
        "./{}-results/processed-aggregated-seq.csv".format(experiment),
        "./{}-results/processed-aggregated-pop.csv".format(experiment),
    ]

    colors = {'mprm': 'orangered',
              'aggregated-seq': 'cadetblue',
              'aggregated-pop': 'goldenrod'}

    labels = {'mprm': 'QRM-MPRM',
              'aggregated-seq': 'Aggregated-QRM-Seq',
              'aggregated-pop': 'Aggregated-QRM-POP'}

    dataframes = {}

    for path in file_paths:
        key = path.split("/")[-1].split(".")[0][10:]
        dataframes[key] = pd.read_csv(path)

    fig, ax = plt.subplots(figsize=(12, 8))

    for key, color in zip(dataframes.keys(), colors):
        df = dataframes[key]
        df['step'] = df['step'] / 1e6
        ax.plot(df['step'], df['median value'], label=labels[key], color=colors[key], linewidth=2)
        ax.fill_between(df['step'], df['first quantile'], df['third quantile'], color=colors[key], alpha=0.5)

    ax.set_xlabel('Steps (in millions)', fontsize=16)
    ax.set_ylabel('Reward', fontsize=16)
    ax.legend(fontsize=16)

    plt.xticks(np.arange(0, 10.1, 1), fontsize=14)
    ax.set_xbound(0, 10)  # set x-axis limits

    plt.yticks(np.arange(-150, -49.9, 10), fontsize=14)
    ax.set_ylim(-150, -50)

    if save_fig:
        plt.savefig("./" + experiment + "-experiment.png", dpi=100)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment', type=str, help="Experiment to plot (one amongst 'bridge', 'gold', and 'gold-gem')")
    parser.add_argument('--save', help="Save plot to a file", action='store_true', required=False)
    argument = parser.parse_args()
    exp = parser.parse_args().experiment

    plot_experiment(exp, argument.save)