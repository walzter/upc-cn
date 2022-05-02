import os
import igraph as ig

def make_graph_config(save:bool, out_dir:str):
    
    graphs = {
        ## ER
        "ER_500_0.2":ig.Graph.Erdos_Renyi(500, p=0.2),
        "ER_750_0.4":ig.Graph.Erdos_Renyi(750, p=0.4),
        "ER_900_0.6":ig.Graph.Erdos_Renyi(1000, p=0.6),
        # ## Barabasi
        "BA_500_3":ig.Graph.Barabasi(n=500, m=3),
        "BA_750_2":ig.Graph.Barabasi(n=750, m=2),
        "BA_1000_2":ig.Graph.Barabasi(n=1000, m=2),
        # ## Watts
        "WS_500_4_0.2":ig.Graph.Watts_Strogatz(dim = 1,size=500, nei=4, p=0.2),
        "WS_750_4_0.4":ig.Graph.Watts_Strogatz(dim = 1,size=750, nei=4, p=0.4),
        "WS_900_4_0.6":ig.Graph.Watts_Strogatz(dim = 1,size=900, nei=4, p=0.6),
        # ## Forest Fire
        "FF_500_0.99":ig.Graph.Forest_Fire(n=500, fw_prob=0.90),
        "FF_750_0.99":ig.Graph.Forest_Fire(n=750, fw_prob=0.90),
        "FF_900_0.99":ig.Graph.Forest_Fire(n=900, fw_prob=0.90),
            }
    ## write the file to pajek 
    format = 'pajek'
    ext = ".net"
    ## saving the graphs
    if save:
        for g in graphs:
            ## check if the file already exists else save it: 
            if not os.path.exists(f"{out_dir}/{g}{ext}"):
                graphs[g].write_pajek(f"{out_dir}/{g}{ext}", format = format)
            else: 
                ig.write(graphs[g], out_dir+"/"+g+ext, format=format)
                
    return graphs