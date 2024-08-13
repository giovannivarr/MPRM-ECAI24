# Maximally Permissive Reward Machines
Repository for the code of the paper "Maximally Permissive Reward Machines". We provide code to run experiments with maximally permissive reward machines and reward machines built from either sequential or partial order plans in the CraftWorld environment, in the three different tasks presented in the paper. 

The implementation is based off of the one that was used for the "[Symbolic Plans as High-Level Instructions for Reinforcement Learning](https://www.cs.toronto.edu/~sheila/publications/illanes-et-al-icaps20.pdf)" paper by Illanes, Yan, Toro Icarte, and McIlraith.

## Requirements
The code can be run using Python 3.11. A file with required packages, `requirements.txt`, can be found in the root folder. Note that these packages are required only to plot the experiments, if you want to run the experiments no external package is required. 

## Running the experiments
You can run the experiments in the terminal from the root folder. Experiments can be run for the three different tasks we present in the paper, the `bridge`, the `gold`, and the `gold-or-gem` tasks. These can be run via the corresponding scripts in the `src/tests` folder: `exp_bridge.py`, `exp_gold.py`, and `exp_gold_gem.py`. Hyperparameters can be set in the `qrm_test` function header in each file, or by specifying them when calling the function in the `main` function. Results of the experiments are saved in the `plots/x-results` folder, where `x` is the task's name.

New maps can be included by adding them in the `src/tests/craft/x-maps` folder, where `x` is the task's name. In order to run experiments on newly defined maps for a task, you have to hardcode these in the corresponding script.

## Plotting the results
To run the scripts via terminal, you have to set the directory to `plots`. Before plotting experiments, the results must be processed via the `process_experiments.py` script in the `plots` folder. Then, the processed results can be plot via the `plot_experiments.py` script in the same folder. 

### Usage 
```
Process experiments usage: python process_experiments.py experiment
	positional argument:
		experiment	Experiment to process (one amongst 'bridge', 'gold', and 'gold-gem')
	
Plot experiments usage: python plot_experiments.py experiment --save
	positional argument:
		experiment	Experiment to plot (one amongst 'bridge', 'gold', and 'gold-gem')
	optional argument:
		--save		Save plot to a file

```