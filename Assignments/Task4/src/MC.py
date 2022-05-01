from collections import defaultdict
from .SIS import SIS
from tqdm import tqdm
import pickle
def MC_SIS(graph_dict: dict, mu_beta_comb:list,n_reps:int, params:dict, save_dir:str):
    ## save all the results
    all_results = defaultdict(defaultdict)
    graphs = defaultdict(defaultdict)
    for graph in (pbar := tqdm(graph_dict)):
        params['g'] = graph_dict[graph]
        graphs[graph] = all_results
        for i in range(n_reps):
            for mu0, beta0 in mu_beta_comb:
                pbar.set_description(f"| Processing | {graph} | Repetition: {i} | Mu: {mu0} | Beta: {beta0} |\t")
                params['mu'] = mu0      ## set the mu to the config file 
                params['beta'] = beta0  ## set the beta to the config file
                ## instantiate the SIS model & simulate)
                rho_ = SIS(**params)._run_simulation() ## returns the average rho 
                if beta0 not in all_results[mu0].keys(): ## if the beta is not in the dictionary
                    graphs[graph][mu0][beta0] = []       ## create a new list for the beta
                    graphs[graph][mu0][beta0].append(rho_) ## append the rho to the list
                else:
                    graphs[graph][mu0][beta0].append(rho_) ## otherwise append the rho to the list
        with open(f'./{save_dir}/{graph}.pickle', 'wb') as handle: ## save the results
            pickle.dump(graphs, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return graphs