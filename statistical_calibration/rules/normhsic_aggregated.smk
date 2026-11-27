rule normhsic_aggregated:    
    input:
        "results/04_statistical_calibration/{dataset}.h5ad",
    output:
        "results/04_statistical_calibration/output/normhsic_aggregated/{dataset}.csv"
    conda:
        "knit_env"
    threads: 10

    benchmark:
        "results/04_statistical_calibration/benchmark/normhsic_aggregated/{dataset}.txt"
    shell:
        """ 
        python statistical_calibration/methods/run_normhsic_aggregated.py -i {input} -o {output}
        """

