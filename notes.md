# Adding normHSIC method to benchmark. 
We run the benchmark for normHSIC independence test as a method to identify spatially variable genes. This is implemented using `knit` package. 
Install from GitHub:
```console
$ pip install git+https://github.com/latt123/knit
```

## Datasets
We did not generate the simulated datasets but imported those used in the original benchmark from [here](https://zenodo.org/records/18193366). 

## Results
For `snakemake_simulate_data` results for the 14 other SVG detection methods are imported from the original benchmark from [here](https://zenodo.org/records/18193366). We run the snakemake pipeline for just `normhsic` method. 

For `statistical_calibration` results for the 14 methods for the original benchmark are not available. We run the snakemake pipeline for `normhsic` (using median bandwidths only and aggregated statistic) and `SPARKX` method.

## Create `knit_env` and `SPARKX_env` conda environment
Conda environments used for `snakemake_simulate_data` and `statistical_calibration` snakemake pipelines. 
```bash
conda env create -f knit_env.yml -n knit_env
```
```bash
conda env create -f SPARKX_env.yml -n SPARKX_env
```
Environment requirements are in `config` folder.

## Modifications to run `normhsic` using snakemake pipeline
We made the following modifications to run `normhsic` method in both the `snakemake_simulate_data` and `statistical_calibration` folders. 

1. In `methods/` add `run_normhsic.py`, a python script to run `normhsic` method. Adding parsers for arguments following template for other methods.
2. In `rules` add `normhsic.smk` file specifying input, output and benchmark paths, conda environment for `knit_env` and shell comand to run `run_normhsic.py` python script.
3. Edit `Snakefile`. Include the `normhsic.smk` file and edit the `method_list` to only run for `normhsic`. Edit the results path in rule. 

For `statistical_calibration` added additional files to run 2 versions of normhsic. One taking just median bandwidths, corresponding to `normhsic` rules and methods and one aggregating p-values over 9 combinations of bandwidth parameters (corresponding to `normhsic_aggregaed` rules and methods.)

## Running `normhsic` varying hyperparameters
To investigate the impact of hyperparameters on the performance of `normhsic` on the `snakemake_simulate_data` section of the benchmark we implement a further snakemake pipeline in `snakemake_simulate_data_comparing_parameters` folder. This requires an additional `normhsic_config.yml` file allowing the method to run several times over the different parameters.  

## Evaluating Simulate Data
We edited the correlation and aupr evaluation notebooks (in `eval_simulate_data` folder) to include `normhsic` as follows
    - Add `normhsic` to the list of methods
    - Edit `compute_correlation` and `compute_aupr` (etc.) functions to include `normhsic`. 
    - Compute results for all datasets in Dataframe. Add variable for technology.

## .gitignore
We modify the .gitignore file to not track results files (h5ad, csv, txt).


## Managing Python Project with uv
