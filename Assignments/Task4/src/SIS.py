## define the class for the SIS model based on numpy
import igraph as ig
import numpy as np
import random

class SIS:
    def __init__(
        self,
        initial_population: int,
        initial_infected_population: float,
        mu: float,
        beta: float,
        seed: int,
        verbose: bool,
    ):
        self.N = initial_population
        self.p = initial_infected_population
        self.init_infected = None
        self.mu = mu
        self.beta = beta
        self.verbose = verbose
        self.start_graph = None
        self.graph = None
        self.layout = None
        self.sis_graph = None
        self.inf_rate = None
        self.seed = (np.random.seed(seed), random.seed(seed))
        

    ## initialize the graph
    def _initiate_network(self) -> ig.Graph:
        """Initiates a Random Graph with the desired parameters"""
        ## we create a random graph
        ## !!!!! CAN ADD DIFFERENT TYPES OF NETWORKS HERE
        g = ig.Graph.Erdos_Renyi(n=self.N, p=0.1)
        layout = g.layout("kk")

        ## Choose a random subset of nodes of size NUM_INFECTED, without replacement
        nodes = np.arange(0,self.N)
        possible_infected_nodes = np.random.uniform(0,1,self.N)
        infected_nodes_idx = nodes[possible_infected_nodes < self.p]
        self.init_infected = len(infected_nodes_idx)
        ## Sus
        susceptible_nodes_idx = np.setdiff1d(nodes, infected_nodes_idx).tolist()
        ## set this attribute to all nodes
        ## ~~ INFECTED
        g.vs[infected_nodes_idx.tolist()]["status"] = "I"  ## set the corresponding label
        g.vs[infected_nodes_idx.tolist()]["color"] = "red"  ## set the corresponding color
        ## ~~ Susceptible
        g.vs[susceptible_nodes_idx]["status"] = "S"
        g.vs[susceptible_nodes_idx]["color"] = "green"
        if self.graph is None:
            self.graph = g  ## set the graph
            self.layout = layout ## set the positions
        ## print some feedback 
        if self.verbose:
            print(f"Number of Nodes: {self.N} | Initial Infected: {self.init_infected} | Initial Susceptible: {len(susceptible_nodes_idx)}")
        return g 

    @staticmethod
    def _update_nodes(
        graph: ig.Graph, inf_nodes: np.array, sus_nodes: np.array
    ) -> ig.Graph:
        """
        Updates the status and color of the node
        """
        ## check, if it is an array, to list 
        ## if it is an int, continue 
        if isinstance(inf_nodes, np.ndarray):
            inf_nodes = inf_nodes.tolist()
        if isinstance(sus_nodes, np.ndarray):
            sus_nodes = sus_nodes.tolist()
        ## update the status
        graph.vs[inf_nodes]["status"] = "I"
        ## update the color
        graph.vs[inf_nodes]["color"] = "red"
        ## update the status
        graph.vs[sus_nodes]["status"] = "S"
        ## update the color
        graph.vs[sus_nodes]["color"] = "green"
        
    ## make a function that returns the list of nodes in a array given a "status" attribute 
    
    def _find_by_attribute(self, graph: ig.Graph, attribute: str, value: str) -> np.array:
        """
        Returns the list of nodes with the given attribute and value
        """
        return np.array([x for x in graph.vs if x[attribute] == value])
    
    ## define a function that given an attribute it sets a given values to it in a node 
    def _set_attribute(self, graph: ig.Graph, attribute: str, value: str, nodes: np.array):
        """
        Sets the attribute to the given value in the nodes
        """
        graph.vs[nodes][attribute] = value

    
    def _run_sis(self) -> ig.Graph:
        """
        runs the SIS model: 
        This function takes the graph and the parameters and returns the updated graph.
        """
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        ## -- STEP 0 : Infected & Susceptible  -- ##
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        inf = self._find_by_attribute(self.graph, "status", "I")  ## Infected Nodes
        sus = self._find_by_attribute(self.graph, "status", "S")  ## Susceptible
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        ## -- STEP 1 : Infected -> Susceptible -- ##
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        recovery_chance = np.random.uniform(
            low=0, high=1, size=inf.shape[0]
        )  ## random chance of recovery
        recovered_nodes = inf[
            recovery_chance < self.mu
        ]  ## if MU is greater than a random number, they become susceptible
        recovered_nodes_idx = [
            x.index for x in recovered_nodes
        ]  ## getting the index of the nodes
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        ## -- STEP 2 : Susceptible -> Infected -- ##
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        possible_new_infected = np.array(
            list(
                [
                    x.index
                    for x in self.graph.vs
                    for y in x.neighbors()
                    if y["status"] == "I"
                ]
            )
        )  ## get all the infected neighbors
        infection_chance = np.random.uniform(
            low=0, high=1, size=len(possible_new_infected)
        )  ## random chance of infection
        new_infected = possible_new_infected[
            infection_chance < self.beta
        ]  ## if BETA is greater than a random number, they become infected
        self._update_nodes(
            graph=self.graph, inf_nodes=new_infected, sus_nodes=recovered_nodes_idx
        )  ## update the nodes
        infection_rate = len(inf) / self.N  ## infection rate
        ## feedback
        if self.verbose:
            ## print the parameters: Population (N), Initial Infected (init_infected), Recovery Rate (mu), Infection Rate (beta)
            print(
                f"Population: {self.N} | Infected (I): {len(inf)} | Susceptible (S): {len(sus)} | Infection Rate: {infection_rate:.2f}"
            )
        self.inf_rate = infection_rate
        self.sis_graph = self.graph
        return self.graph, infection_rate

    ## make the pipeline to run all: _initiate_network, _run_sis
    def _model(self) -> ig.Graph:
        """Runs the entire SIS model"""
        ## Init the network 
        sis_graph,infection_rate = self._run_sis(self, graph=self.graph, beta=self.beta, mu=self.mu)
        ## return the sis_graph and the infected rate 
        return self.graph,sis_graph, infection_rate
        
    def _info(self):
        print(
            f"Number of Nodes: {self.N} | Initial Infected: {self.init_infected} | Recovery Rate: {self.mu} | Transmission Rate: {self.beta}"
        )

    def _results(self):
        print(
            f"Number of Nodes: {self.N} | Initial Infected: {self.init_infected} | Recovery Rate: {self.mu} | Transmission Rate: {self.beta} | Final Infection Rate: {self.inf_rate:.2f}"
        )
        
        
