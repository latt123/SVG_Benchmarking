rule normhsic:    
    input:
        "results/01_generate_simulate_data/{dataset}.h5ad",
    output:
        "results/02_snakemake_simulate_data/output/normhsic/{dataset}.csv"
    conda:
        "knit_env"
    threads: 10

    benchmark:
        "results/02_snakemake_simulate_data/benchmark/normhsic/{dataset}.txt"
    shell:
        """ 
        python snakemake_simulate_data/methods/run_normhsic.py -i {input} -o {output}
        """