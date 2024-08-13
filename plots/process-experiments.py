import argparse
import sys
from collections import defaultdict
from numpy import array, append, zeros, quantile

N = 10

def process_mprm(experiment: str):
    out_path = "./{}-results/processed-mprm.csv".format(experiment)

    out_data = defaultdict(lambda: array([]))
    for i in range(0, 10):
        with open("./{}-results/mprm-{}{}.csv".format(experiment, experiment, i)) as f:
            windowy = zeros(N)
            j = 0
            previous_step = None
            for line in f:
                data = line.split()

                # there's a bug somewhere because I get duplicated lines every now and then
                if int(data[0]) == previous_step:
                    continue
                previous_step = int(data[0])

                if int(data[0]) == 0:
                    j = 0
                    out_data[int(data[0])] = append(out_data[int(data[0])], float(data[1]))
                    continue
                windowy[j] = float(data[1])
                j += 1
                if j == N:
                    out_data[int(data[0])] = append(out_data[int(data[0])], windowy.mean())
                    j = 0

    with open(out_path, "w") as out:
        out.write("step,first quantile,median value,third quantile\n")
        for step, values in out_data.items():
            out.write("{},{},{},{}\n".format(step, quantile(values, 0.25),
                                             quantile(values, 0.5), quantile(values, 0.75)))


def collect_data(experiment: str, agent: str):
    out_data = defaultdict(lambda: array([]))

    for i in range(0, 10):
        with open("./{}-results/{}-{}{}.csv".format(experiment, agent, experiment, i)) as f:
            windowy = zeros(N)
            j = 0
            previous_step = None
            for line in f:
                data = line.split()

                # For some reason a few lines are duplicated sometimes
                if int(data[0]) == previous_step:
                    continue
                previous_step = int(data[0])

                if int(data[0]) == 0:
                    j = 0
                    out_data[int(data[0])] = append(out_data[int(data[0])], float(data[1]))
                    continue
                windowy[j] = float(data[1])
                j += 1
                if j == N:
                    out_data[int(data[0])] = append(out_data[int(data[0])], windowy.mean())
                    j = 0

    return out_data


def aggregate_seq(experiment: str):
    out_path = "./{}-results/processed-aggregated-seq.csv".format(experiment)

    if experiment == 'gold-gem':
        out_data_0 = collect_data(experiment, 'seq0')
        out_data_1 = collect_data(experiment, 'seq1')
        out_data_2 = collect_data(experiment, 'seq2')
        out_data_3 = collect_data(experiment, 'seq3')
        out_data_4 = collect_data(experiment, 'seq4')
        out_data_5 = collect_data(experiment, 'seq5')
        out_data_6 = collect_data(experiment, 'seq6')

        with open(out_path, "w") as out:
            out.write("step,first quantile,median value,third quantile\n")
            for step in out_data_0.keys():
                quantile_1 = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step], out_data_3[step],
                     out_data_4[step], out_data_5[step], out_data_6[step]], 0.25)
                median = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step], out_data_3[step],
                     out_data_4[step], out_data_5[step], out_data_6[step]], 0.5)
                quantile_3 = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step], out_data_3[step],
                    out_data_4[step], out_data_5[step], out_data_6[step]], 0.75)
                out.write("{},{},{},{}\n".format(step, quantile_1, median, quantile_3))

    else:
        out_data_0 = collect_data(experiment, 'seq0')
        out_data_1 = collect_data(experiment, 'seq1')
        out_data_2 = collect_data(experiment, 'seq2')
        out_data_3 = collect_data(experiment, 'seq3')

        with open(out_path, "w") as out:
            out.write("step,first quantile,median value,third quantile\n")
            for step in out_data_0.keys():
                quantile_1 = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step], out_data_3[step]], 0.25)
                median = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step], out_data_3[step]], 0.5)
                quantile_3 = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step], out_data_3[step]], 0.75)
                out.write("{},{},{},{}\n".format(step, quantile_1, median, quantile_3))


def aggregate_pop(experiment: str):
    out_path = "./{}-results/processed-aggregated-pop.csv".format(experiment)

    if experiment == 'gold-gem':
        out_data_0 = collect_data(experiment, 'pop0')
        out_data_1 = collect_data(experiment, 'pop1')
        out_data_2 = collect_data(experiment, 'pop2')

        with open(out_path, "w") as out:
            out.write("step,first quantile,median value,third quantile\n")
            for step in out_data_0.keys():
                quantile_1 = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step]], 0.25)
                median = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step]], 0.5)
                quantile_3 = quantile(
                    [out_data_0[step], out_data_1[step], out_data_2[step]], 0.75)
                out.write("{},{},{},{}\n".format(step, quantile_1, median, quantile_3))

    else:
        out_data_0 = collect_data(experiment, 'pop0')
        out_data_1 = collect_data(experiment, 'pop1')

        with open(out_path, "w") as out:
            out.write("step,first quantile,median value,third quantile\n")
            for step in out_data_0.keys():
                quantile_1 = quantile(
                    [out_data_0[step], out_data_1[step]], 0.25)
                median = quantile(
                    [out_data_0[step], out_data_1[step]], 0.5)
                quantile_3 = quantile(
                    [out_data_0[step], out_data_1[step]], 0.75)
                out.write("{},{},{},{}\n".format(step, quantile_1, median, quantile_3))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment', type=str, help="Experiment to process (one amongst 'bridge', 'gold', and 'gold-gem')")
    exp = parser.parse_args().experiment

    process_mprm(exp)
    aggregate_seq(exp)
    aggregate_pop(exp)