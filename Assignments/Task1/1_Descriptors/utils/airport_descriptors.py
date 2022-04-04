import igraph 
import pandas as pd
import pickle
import numpy as np

def load_pickle(file:str) -> np.array:
    """"""
    ## context manager 
    with open(file, "rb") as open_file:
        data = pickle.load(open_file)
    ## load to df 
    df = pd.DataFrame(data).T.reset_index()
    df = df.rename(columns={"index":"Airport"})
    ## return the mean, max length 
    return df['avg_len'].values, df['max_len'].values


class AirportDescriptor:
    """
    Calculates Descriptors for a given graph 
    
    What can be changed?
    - Loaded Graph 
    - Number of decimal points to round 
    - If provided, a pickle file with the calculated distances (avoid unnecesary re-computation)
    
    Returns a Dictionary with the following info per node / Vertex
    - Name
    - Weight 
    - Degree
    - Strength
    - Clustering Coefficient (Transitivity)
    - Average Path Length 
    - Maximum Path Length 
    - Eigenvector Centrality 
    - Betweenness 
    - PageRank
    
    """
    def __init__(self, loaded_graph:igraph.Graph,) -> pd.DataFrame:
        """Object to calculate all the descriptors for the real graph"""
        self.model = loaded_graph 
        self.decimals = 8
        self.pickle_file = "./distances.pickle"
        # pass the list of airports 
        self.names = [x['name'] for x in self.model.vs()]
        # weights 
        self.weights = [x['weight'] for x in self.model.es()]
        # degrees 
        self.degree = [self.model.degree(vertices=v['id']) for v in self.model.vs()]
        # strenghts 
        self.strength = [self.model.strength(vertices=v['id']) for v in self.model.vs()]
        ## clustering coefficient 
        self.cluster_coef = [self.model.transitivity_local_undirected(vertices=v['id']) for v in self.model.vs()]
        ## average path length 
        self.avg_path, self.max_len = load_pickle(self.pickle_file)
        ## eigenvector centrality 
        self.eigen_centrality = self.model.eigenvector_centrality(directed=False)
        #self.eigen_cent_rounded = list(map(lambda x: round(x, self.decimals),self.eigen_centrality))
        # betweenness 
        self.between = self.model.betweenness(self.names, directed=False)
        #self.between_rounded = list(map(lambda x: round(x, self.decimals), self.between))
        # pagerank
        self.page_rank = self.model.pagerank()
        #self.page_rank_rounded = list(map(lambda x: round(x, self.decimals), self.page_rank))
    

    
    def _summary(self):
        
        network_dict = {
                        "Airport":self.names,
                        "Degree":self.degree,
                        "Strength":self.strength, 
                        "Cluster_Coefficient":self.cluster_coef,
                        "Average Length": self.avg_path,
                        "Max Length": self.max_len,
                        "EigenVector Centrality":self.eigen_centrality,
                        "Betweenness": self.between,
                        "PageRank":self.page_rank,
                        }
        
        return network_dict