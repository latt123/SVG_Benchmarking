
rule SPARKX:    
    input:
        "results/04_statistical_calibration/{dataset}.h5ad",
    output:
        "results/04_statistical_calibration/output/SPARKX/{dataset}.csv"
    conda:
        "SPARKX_env"
    threads: 10

    benchmark:
        "results/04_statistical_calibration/benchmark/SPARKX/{dataset}.txt"
    shell:
        "Rscript statistical_calibration/methods/run_SPARK-X.R -i {input} -o {output}"
