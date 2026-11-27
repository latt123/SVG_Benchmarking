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
        "--truncation",
        type = int,
        default=None,
        help="Truncations for Cov X and Cov E",
    )

    parser.add_argument(
        "--kernel_X",
        type = str,
        default=None,
        help="Kernel for X",
    )

    parser.add_argument(
        "--kernel_Y",
        type = str,
        default=None,
        help="Kernel for Y",
    )

    parser.add_argument(
        "--q_X",
        type = float,
        default=None,
        help="Quantiles for bandwidth for kernel X",
    )

    parser.add_argument(
        "--q_Y",
        type = float,
        default=None,
        help="Quantiles for bandwidth for kernel Y",
    )
    parser.add_argument(
        "--proportion_train",
        type = float,
        default=None,
        help="Proportion of training data",
    )    

    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output filename for results"
    )

    return parser.parse_args()




def main():
    args = parse_args()
    adata = sc.read_h5ad(args.input)


    # parameters from args
    kernel_X = args.kernel_X
    kernel_Y = args.kernel_Y
    truncation_X, truncation_e = args.truncation, args.truncation
    q_X = args.q_X
    q_Y = args.q_Y
    proportion_train = args.proportion_train


    ## Extract X and Y from adata
    X = adata.obsm['spatial']
    Y_all_genes = adata.layers['counts'].toarray()
    ## Extract spatial var and gene names
    spatial_var_list = adata.var['spatial_var'].values
    gene_list = adata.var['gene'].values
    values_df = []
    ## Run test on each gene
    for i in range(Y_all_genes.shape[1]):
        pval, test_stat = run_test(X,Y_all_genes[:,i],  kernel_X = kernel_X, kernel_Y = kernel_Y, 
        quantiles_bandwidth_X = [q_X], quantiles_bandwidth_Y = [q_Y], 
        projection_X = 'pls', truncation_X = truncation_X, truncation_e  = truncation_e,
        output_projections  = False, proportion_train = proportion_train, centre_scale = False)
        if test_stat > 10**10:
            print(f'ERROR, test stat = {test_stat}')
            test_stat = 0
            pval = 1
        values_df.append([gene_list[i], spatial_var_list[i], pval, test_stat])    
        if (i+1)%50 == 0:
            print(f'{i+1}/{Y_all_genes.shape[1]}')
    ## Create dataframe
    columns_df = ['gene', 'spatial_var', 'pval', 'test_stat']
    df = pd.DataFrame(values_df, columns = columns_df)

    ## Output dataframe as csv
    df.to_csv(args.output)


# Needs to be at the end of the script
if __name__ == "__main__":
    main()








# If running on one set of parameters:

# def main():
#     args = parse_args()

#     adata = sc.read_h5ad(args.input)
#     X = adata.obsm['spatial']
#     Y_all_genes = adata.layers['counts'].toarray()

#     n_genes = Y_all_genes.shape[1]
#     pvals = np.zeros(n_genes)
#     max_test_stats = np.zeros(n_genes)
#     for i_gene in range(n_genes):
#         Y = Y_all_genes[:,i_gene]
#         pval_agg, max_test_stat, pval_array = run_test(X,Y)
#         pvals[i_gene] = pval_agg
#         max_test_stats[i_gene] = max_test_stat 

#     df = pd.DataFrame({
#         'gene': adata.var['gene'],
#         'spatial_var': adata.var['spatial_var'],
#         'aggregated_pval': pvals,
#         'max_test_stat': max_test_stats})

#     df.to_csv(args.output)



# For running different combinations of parameters
# truncation_list = [[1,1], [2,2], [4,4]]
# q_bandwidth_X_list = [0.05, 0.1, 0.5]
# q_bandwidth_Y_list = [0.25, 0.5, 0.75]



# def main():
#     args = parse_args()
#     adata = sc.read_h5ad(args.input)
#     kernel_X = args.kernel_X
#     kernel_Y = args.kernel_Y
#     df = run_test_parameters(adata, kernel_X, kernel_Y, truncation_list, q_bandwidth_X_list, q_bandwidth_Y_list)
#     df.to_csv(args.output)



# def run_test_parameters(adata, kernel_X, kernel_Y, truncation_list, q_bandwidth_X_list, q_bandwidth_Y_list):
#     """
#     For fixed kernels, run test over truncation and bandwidth parameters for all genes in dataset. Output dataframe.

#     Args:
#         dataset (str): name of dataset
#         kernel_X (str): kernel function for X
#         kernel_Y (str): kernel function for Y
#         truncation_list (list): list of truncation parameters, for truncation_X and truncation_e
#         q_bandwidth_X_list (list): list of bandwidth parameters for X
#         q_bandwidth_Y_list (list): list of bandwidth parameters for Y
    
#     Returns:
#         df (pandas.DataFrame): dataframe of results

#     """
#     X = adata.obsm['spatial']
#     Y_all_genes = adata.layers['counts'].toarray()
#     spatial_var_list = adata.var['spatial_var'].values
#     gene_list = adata.var['gene'].values

#     values_df = []
#     for i in range(Y_all_genes.shape[1]):
#         for truncation_X, truncation_e in truncation_list:
#             for q_bandwidth_X in q_bandwidth_X_list:
#                 for q_bandwidth_Y in q_bandwidth_Y_list:
#                         pval, test_stat, pval_array = run_test(X,Y_all_genes[:,i], kernel_X = kernel_X, kernel_Y = kernel_Y)
#                         values_df.append([gene_list[i], spatial_var_list[i], pval, test_stat, truncation_X, truncation_e, q_bandwidth_X, q_bandwidth_Y])    


#     columns_df = ['gene', 'spatial_var','pval', 'test_stat', 'truncation_X', 'truncation_e', 'q_bandwidth_X', 'q_bandwidth_Y']
#     df = pd.DataFrame(values_df, columns = columns_df)
#     return df

    # parser.add_argument(
    #     "--kernel_X",
    #     type=str,
    #     default=None,
    #     help="Kernel for X",
    # )
    # parser.add_argument(
    #     "--kernel_Y",
    #     type=str,
    #     default=None,
    #     help="Kernel for Y",
    # )