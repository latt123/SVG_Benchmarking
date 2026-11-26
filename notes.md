# Adding normHSIC method to benchmark. 

We run the benchmark for normHSIC independence test as a method to identify spatially variable genes. This is implemented using `knit` package. 
Install from GitHub:
```console
$ pip install git+https://github.com/latt123/knit
```

**Datasets**
We did not generate the simulated datasets but imported those used in the original benchmark from [here](https://zenodo.org/records/18193366). 

**Results**
For `snakemake_simulate_data` results for the 14 other SVG detection methods are imported from the original benchmark from [here](https://zenodo.org/records/18193366). We run the snakemake pipeline for just `normhsic` method. 

For `statistical_calibration` results for the 14 methods for the original benchmark are not available. We run the snakemake pipeline for `normhsic` and `SPARKX` method.

**Create `knit_env` and `SPARKX_env` conda environment:**
Conda environments used for `snakemake_simulate_data` and `statistical_calibration` snakemake pipelines. 
```bash
conda env create -f knit_env.yml -n knit_env
```
```bash
conda env create -f SPARKX_env.yml -n SPARKX_env
```
Environment requirements are in `config` folder.


**Adding `normhsic` to snakemake pipeline**


**.gitignore**
We modify the .gitignore file to not track results files (h5ad, csv, txt).