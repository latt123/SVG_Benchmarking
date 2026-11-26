rule knit:    
    input:
        "results/01_generate_simulate_data/{dataset}.h5ad",
    output:
        "results/02b_snakemake_simulate_data_comparing_parameters/output/knit/{dataset}_trunc_{truncation}_kX_{kernel_X}_kY_{kernel_Y}_qX_{q_X}_qY_{q_Y}_proptrain_{proportion_train}.csv"
    conda:
        "knit_env"
    threads: 10
    params:
        truncation="{truncation}",
        kernel_X="{kernel_X}",
        kernel_Y="{kernel_Y}",
        q_X="{q_X}",
        q_Y="{q_Y}",
        proportion_train="{proportion_train}",

    benchmark:
        "results/02b_snakemake_simulate_data_comparing_parameters/benchmark/knit/{dataset}_trunc_{truncation}_kX_{kernel_X}_kY_{kernel_Y}_qX_{q_X}_qY_{q_Y}_proptrain_{proportion_train}.txt"
    shell:
        """ 
        python snakemake_simulate_data_comparing_parameters/methods/run_knit.py -i {input} --truncation {params.truncation} --kernel_X {params.kernel_X} --kernel_Y {params.kernel_Y} --q_X {params.q_X} --q_Y {params.q_Y} --proportion_train {params.proportion_train} -o {output}
        """