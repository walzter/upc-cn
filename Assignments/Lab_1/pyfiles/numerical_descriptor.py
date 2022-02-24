import igraph 
import numpy as np 

class NumericalGraphDescriptor:
    """
    File --> Load --> Graph --> Do some Statistics --> Output File
    """
    def __init__(self , in_file: str) -> dict:
        self.in_file = in_file.split('/')[-1]
        self.graph = igraph.read(in_file, format='pajek')
        self.folder = in_file.split('/')[1]
        self.decimals = 4
        self.nodes = 0
        self.edges = 0
        self.density = 0
        self.avg_path_len = 0
        self.ast = 0
        self.diam = 0
        self.min_degree = 0 
        self.max_degree = 0
        
    # number of edges
    def _get_edges(self) -> int:
        return self.graph.ecount()
    # number of vertices 
    def _get_vertices(self) -> int:
        return self.graph.vcount()
    # density 
    def _get_density(self) -> float:
        return round(self.graph.density(), self.decimals)
    # average path length 
    def _avg_path_len(self) -> float:
        return round(self.graph.average_path_length(), self.decimals)
        #return self.graph.average_path_length()
    # Assortativity
    def _assortativity(self) -> float:
        return round(self.graph.assortativity_degree(), self.decimals)
    # diameter 
    def _diameter(self) -> int:
        return self.graph.diameter()
    # min degrees 
    def _min_degree(self) -> int:
        return np.min(self.graph.degree())
    # max degree
    def _max_degree(self) -> int:
        return np.max(self.graph.degree())
    # avg degree
    def _avg_degree(self) -> float:
        return round(np.mean(self.graph.degree()), self.decimals)
    def _transitivity(self) -> float:
        return round(self.graph.transitivity_avglocal_undirected(), self.decimals)
    # putting it all together 
    def _summary(self) -> dict:
        d = {
                "FileName":self.in_file,
                "Folder": self.folder,
                "Edges":self._get_edges(),
                "Nodes":self._get_vertices(),
                "Density":self._get_density(),
                "Avg. Path Length":self._avg_path_len(),
                "Assortativity":self._assortativity(),
                "Diameter":self._diameter(),
                "Transitivity": self._transitivity(),
                "Min. Degree":self._min_degree(),
                "Avg. Degree":self._avg_degree(),
                "Max. Degree":self._max_degree(),
            }
        return d