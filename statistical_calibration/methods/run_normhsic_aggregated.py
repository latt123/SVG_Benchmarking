import pandas as pd
import numpy as np
import scanpy as sc
from knit.run_test import run_test
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run normhsic with command line")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=None,
        help="Input filename, must be an Anndata object",
    )
    parser.add_argument(
        "--kernel_X",
        type=str,
        default=None,
        help="Kernel for X",
    )
    parser.add_argument(
        "--kernel_Y",
        type=str,
        default=None,
        help="Kernel for Y",
    )


    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output filename for results"
    )

    return parser.parse_args()


# quantiles to aggregate over
quantiles_bandwidth_X = [0.01, 0.1, 0.5]
quantiles_bandwidth_Y = [0.25, 0.5, 0.75]
truncation_X = 2
truncation_e = 4
proportion_train = 0.3  

# For running different combinations of parameters

def main():
    args = parse_args()
    adata = sc.read_h5ad(args.input)
    ## Extract X and Y from adata
    X = adata.obsm['spatial']
    Y_all_genes = adata.layers['counts'].toarray()
    ## Extract gene names
    gene_list = adata.var.index.values
    values_df = []
    ## Run test on each gene
    for i in range(Y_all_genes.shape[1]):
            try_count = 0
            test_stat = 0
            while (try_count < 5)&(test_stat == 0):
                pval, test_stat = run_test(X,Y_all_genes[:,i],  kernel_X = 'gaussian', kernel_Y = 'gaussian', 
                quantiles_bandwidth_X = quantiles_bandwidth_X, quantiles_bandwidth_Y = quantiles_bandwidth_Y, 
                projection_X = 'pls', truncation_X = truncation_X, truncation_e  = truncation_e, output_projections  = False, 
                proportion_train = proportion_train, centre_scale = False)
                try_count += 1
                if test_stat > 10**10:
                    print(f'ERROR, test stat = {test_stat}')
            values_df.append([gene_list[i], pval, test_stat, truncation_X, truncation_e, quantiles_bandwidth_X, quantiles_bandwidth_Y,  proportion_train])    
            if (i+1)%1 == 0:
                print(f'{i+1}/{Y_all_genes.shape[1]}')

    ## Create dataframe
    columns_df = ['gene', 'pval', 'test_stat', 'truncation_X', 'truncation_e', 'q_bandwidth_X', 'q_bandwidth_Y', 'proportion_train']
    df = pd.DataFrame(values_df, columns = columns_df)

    ## Output dataframe as cs
    df.to_csv(args.output)

# Needs to be at the end of the script
if __name__ == "__main__":
    main()



