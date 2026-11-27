import pandas as pd
import scanpy as sc
from knit.run_test import run_test
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run knit with command line")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=None,
        help="Input filename, must be an Anndata object",
    )

    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output filename for results"
    )

    return parser.parse_args()




def main():
    args = parse_args()
    adata = sc.read_h5ad(args.input)

    ## Extract X and Y from adata
    X = adata.obsm['spatial']
    Y_all_genes = adata.layers['counts'].toarray()
    ## Extract spatial var and gene names
    spatial_var_list = adata.var['spatial_var'].values
    gene_list = adata.var['gene'].values
    values_df = []
    ## Run test on each gene
    for i in range(Y_all_genes.shape[1]):
        try_count = 0
        test_stat = 0
        while (try_count < 5)&(test_stat == 0):
            pval, test_stat = run_test(X,Y_all_genes[:,i],  kernel_X = 'gaussian', kernel_Y = 'gaussian', 
            quantiles_bandwidth_X = [0.01, 0.1, 0.5], quantiles_bandwidth_Y = [0.25, 0.5, 0.75], 
            projection_X = 'pls', truncation_X = 2, truncation_e  = 4, output_projections  = False, 
            proportion_train = 0.3, centre_scale = False)
            try_count += 1
            if test_stat > 10**10:
                print(f'ERROR, test stat = {test_stat}')
        values_df.append([gene_list[i], spatial_var_list[i], pval, test_stat])    
        if (i+1)%10 == 0:
            print(f'{i+1}/{Y_all_genes.shape[1]}')
    ## Create dataframe
    columns_df = ['gene', 'spatial_var', 'pval', 'test_stat']
    df = pd.DataFrame(values_df, columns = columns_df)

    ## Output dataframe as csv
    df.to_csv(args.output)


# Needs to be at the end of the script
if __name__ == "__main__":
    main()





