rule normhsic:    
    input:
        "results/04_statistical_calibration/{dataset}.h5ad",
    output:
        "results/04_statistical_calibration/output/normhsic/{dataset}.csv"
    conda:
        "knit_env"
    threads: 10

    benchmark:
        "results/04_statistical_calibration/benchmark/normhsic/{dataset}.txt"
    shell:
        """ 
        python statistical_calibration/methods/run_normhsic.py -i {input} -o {output}
        """

