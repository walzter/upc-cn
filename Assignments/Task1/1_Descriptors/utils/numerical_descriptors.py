import numpy as np 
import igraph 

class NumericalNetworkDescriptor:
    """ Loads .net file and calculates arbitrary Numerical Descriptors of the Networks.
    
    PARAMETERS:
    -----------
    dataset : name of the dataset 
    file_name : name of the model 
    loaded_model : igraph model loaded in memory 
    

    
    RETURNS:
    --------
    d : dict
        returns the summary of the loaded network in a dictionary. 
    
    """
    def __init__(self, dataset:str, file_name:str, loaded_graph:igraph.Graph) -> dict:
        self.dataset = dataset 
        self.file_name = file_name
        #self.graph = igraph.read(in_file, format='pajek')
        self.graph = loaded_graph[0]
        self.decimals = 4
        # number of edges
        self.edges = self.graph.ecount()
        # number of vertices 
        self.vertices = self.graph.vcount()
        # density 
        #self.density = round(self.graph.density(), self.decimals) 
        # average path length 
        self._avg_path_len = round(self.graph.average_path_length(), self.decimals)
        # average degree
        self.average_degree = round(np.mean(self.graph.degree()), self.decimals)
        # min degree 
        self.min_degree = np.min(self.graph.degree())
        # max degree 
        self.max_degree = self.graph.maxdegree()
        # transitivity - average cluster coefficient per node 
        self.avg_transitivity = round(self.graph.transitivity_avglocal_undirected(), self.decimals)
        # assortativity 
        self.assortativity = round(self.graph.assortativity_degree(), self.decimals)
        # diameter 
        self.diameter = round(self.graph.diameter(), self.decimals)
        
    def _summary(self) -> dict:
        graph_data_summary = {
                "File_Name":self.file_name,
                "Folder": self.dataset,
                "Edges":self.edges,
                "Nodes":self.vertices,
                "Avg. Path Length":self._avg_path_len,
                "Assortativity":self.assortativity,
                "Diameter":self.diameter,
                "Transitivity_cluster_coefficient": self.avg_transitivity,
                "Min. Degree":self.min_degree,
                "Avg. Degree":self.average_degree,
                "Max. Degree":self.max_degree,
            }
        return graph_data_summary
    