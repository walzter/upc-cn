## define the class for the SIS model based on numpy 
import igraph as ig
import numpy as np 

class SIS:
    def __init__(self,
                 initial_population:int,
                 initial_infected_population:float,
                 mu:float,
                 beta:float,
                 verbose:bool,
                 ):
        self.N = initial_population
        self.init_infected = int(initial_infected_population * self.N)
        self.mu = mu 
        self.beta = beta
        self.verbose = verbose
        self.graph = None
        self.inf_rate = None
        
        
    ## initialize the graph
    def _initiate_network(self) -> ig.Graph:
        """Initiates a Random Graph with the desired parameters"""
        ## we create a random graph 
        ## !!!!! CAN ADD DIFFERENT TYPES OF NETWORKS HERE 
        g = ig.Graph.Erdos_Renyi(n=self.N,p=0.02)
        
        ## Choose a random subset of nodes of size NUM_INFECTED, without replacement
        ## inf
        infected_nodes = np.random.choice(g.vs, size=self.init_infected, replace=False)
        infected_nodes_idx = [x.index for x in infected_nodes] ## getting their index 
        ## Sus
        susceptible_nodes = [x for x in g.vs if x.index not in infected_nodes_idx] ## getting the susceptible nodes
        susceptible_nodes_idx = [x.index for x in susceptible_nodes] ## getting their index
        
        ## set this attribute to all nodes
        ## ~~ INFECTED
        g.vs[infected_nodes_idx]["status"] = "I" ## set the corresponding label
        g.vs[infected_nodes_idx]["color"] = "red" ## set the corresponding color
        ## ~~ Susceptible
        g.vs[susceptible_nodes_idx]['status'] = "S"
        g.vs[susceptible_nodes_idx]["color"] = "green"
        self.graph = g ## set the graph
        return g
    
    @staticmethod
    def _update_nodes(graph:ig.Graph, inf_nodes:np.array, sus_nodes:np.array) -> ig.Graph:
        """
        Updates the status and color of the node 
        """
        inf_nodes, sus_nodes = list(inf_nodes), list(sus_nodes)
        ## update the status 
        graph.vs[inf_nodes]['status'] = "I"
        ## update the color 
        graph.vs[inf_nodes]['color'] = "red"
        ## update the status 
        graph.vs[sus_nodes]['status'] = "S"
        ## update the color 
        graph.vs[sus_nodes]['color'] = "green"
        
    def _info(self):
        print(f"Number of Nodes: {self.N} | Initial Infected: {self.init_infected} | Recovery Rate: {self.mu} | Transmission Rate: {self.beta}")
    
    def _results(self):
        print(f"Number of Nodes: {self.N} | Initial Infected: {self.init_infected} | Recovery Rate: {self.mu} | Transmission Rate: {self.beta} | Final Infection Rate: {self.inf_rate:.2f}")
    
    def _run_sis(self):
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        ## -- STEP 0 : Infected & Susceptible  -- ##
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        inf = np.array([x for x in self.graph.vs if x['status'] == 'I']) ## Infected Nodes
        sus = np.array([x for x in self.graph.vs if x['status'] == 'S']) ## Susceptible 
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        ## -- STEP 1 : Infected -> Susceptible -- ##
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        recovery_chance = np.random.uniform(low=0,high=1,size=inf.shape[0]) ## random chance of recovery
        recovered_nodes = inf[recovery_chance < self.mu] ## if MU is greater than a random number, they become susceptible
        recovered_nodes_idx = [x.index for x in recovered_nodes] ## getting the index of the nodes 
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        ## -- STEP 2 : Susceptible -> Infected -- ##
        ## -- -- -- -- -- -- -- -- -- -- -- -- -- ##
        possible_new_infected = np.array(list([x.index for x in self.graph.vs for y in x.neighbors() if y['status'] == 'I'])) ## get all the infected neighbors
        infection_chance = np.random.uniform(low=0, high = 1, size = len(possible_new_infected)) ## random chance of infection
        new_infected = possible_new_infected[infection_chance < self.beta] ## if BETA is greater than a random number, they become infected
        self._update_nodes(graph=self.graph, inf_nodes = new_infected, sus_nodes = recovered_nodes_idx) ## update the nodes 
        infection_rate = len(inf)/self.N ## infection rate
        ## feedback 
        if self.verbose: 
            ## print the parameters: Population (N), Initial Infected (init_infected), Recovery Rate (mu), Infection Rate (beta)
            print(f"Population: {self.N} | Infected (I): {len(inf)} | Susceptible (S): {len(sus)} | Infection Rate: {infection_rate:.2f}")
        self.inf_rate = infection_rate
        self.mod_graph = self.graph
        return self.mod_graph
    ## clear the sessions