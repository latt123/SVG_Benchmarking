rule knit:    
    input:
        "results/01_generate_simulate_data/{dataset}.h5ad",
    output:
        "results/02_snakemake_simulate_data/output/knit/{dataset}.csv"
    conda:
        "knit_env"
    threads: 10

    benchmark:
        "results/02_snakemake_simulate_data/benchmark/knit/{dataset}.txt"
    shell:
        """ 
        python snakemake_simulate_data/methods/run_knit.py -i {input} -o {output}
        """