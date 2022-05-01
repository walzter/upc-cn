## define the class for the SIS model based on numpy
import igraph as ig
from termcolor import colored
import numpy as np
import random

class SIS2:
    def __init__(
        self,
        g: ig.Graph,
        initial_population: int,
        initial_infected_population: float,
        mu: float,
        beta: float,
        n_iter:int,
        seed: int,
        verbose: bool,
    ):
        self.N = initial_population
        self.P = initial_infected_population
        self.mu = mu
        self.beta = beta
        self.n_iter = n_iter
        self.t_trans = 100
        self.graph = g
        self.layout = None
        self.sis_graph = None
        self.inf_rate = [None] * self.n_iter
        self.init_infected = None
        self.seed = (np.random.seed(seed), random.seed(seed))
        self.verbose = verbose
    
    
    
    
    def _start_network(self) ->ig.Graph:
        """
        Initiates the Random Graph with the desired parameters.
        Sets the infected & susceptible nodes in the graph. 
        """
        #g = self.graph
        #g = ig.Graph.Erdos_Renyi(self.N, p=0.2)
        ## Choose a random subset of nodes of size NUM_INFECTED, without replacement
        nodes = np.arange(0,self.N)
        infected_nodes_idx = np.random.choice(nodes, size=int(self.P*self.N), replace=False)
        self.init_infected = infected_nodes_idx
        ## Sus
        susceptible_nodes_idx = np.setdiff1d(nodes, infected_nodes_idx).tolist()
        ## set this attribute to all nodes
        ## ~~ INFECTED
        #g.vs[infected_nodes_idx.tolist()]["status"] = "I"  ## set the corresponding label
        #g.vs[infected_nodes_idx.tolist()]["color"] = "red"  ## set the corresponding color
        ## ~~ Susceptible
        #g.vs[susceptible_nodes_idx]["status"] = "S"
        #g.vs[susceptible_nodes_idx]["color"] = "green"
        if self.verbose:
            print(f"Number of Nodes: {self.N} | Initial Infected: {len(self.init_infected)} | Initial Susceptible: {len(susceptible_nodes_idx)}")
        return g

    @staticmethod
    def _get_infected_neighbors(node_list: list, beta: float) -> np.array:
        """
        Returns the list of infected neighbors of the given node list
        """
        infected_neighbors = []
        for node in node_list:
            neighbors = np.array([x for x in node.neighbors() if x["status"] == "I"])
            for _ in neighbors:
                possible_infection = np.random.uniform(0,1)
                if possible_infection < beta:
                    infected_neighbors.append(node)
                    break
        return np.array(infected_neighbors)

    @staticmethod
    def _update_nodes(graph: ig.Graph, node_list: np.array, status: str) -> ig.Graph:
        """
        Updates the status and color of the given node list.
        """
        ## check, if it is an array, to list 
        ## if it is an int, continue 
        if isinstance(node_list, np.ndarray):
            node_list = node_list.tolist()
        ## update the status
        if status == "I":
            graph.vs[node_list]["status"] = "I"
            ## update the color
            graph.vs[node_list]["color"] = "red"
        elif status == "S":
            ## update the status
            graph.vs[node_list]["status"] = "S"
            ## update the color
            graph.vs[node_list]["color"] = "green"
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

    
    def _run_simulation(self):#, g:ig.Graph):
        ######################################################## START FEEDBACK #################################################################
        if self.verbose:
            dashes = "+ - - - - - - - - " * 6 + "+"
            title = colored("Summary Statistics:",attrs=['bold'])
            params = colored(f"Parameters: Population = {self.N}, Beta = {self.beta}, Mu = {self.mu}, p = {self.P}",attrs=['bold'])
            print(title);print(params);print(dashes)
            txt_it = "Iteration"
            txt_inf = "Infected"
            txt_sus = "Susceptible"
            txt_s2i = "S -> I"
            txt_i2s = "I -> S"
            txt_ir = "Infected Ratio"
            hd_txt = f"| {txt_it:^15s} | {txt_inf:^15s} | {txt_sus:^15s} | {txt_s2i:^15s} | {txt_i2s:^15s} | {txt_ir:^15s} |"
            #hd_txt = "|\tIteration\t|\tInfected\t|\tSusceptible\t|\tSusceptible to Infected\t|\tInfected to Susceptible\t|\tInfection Rate\t|"
            header = colored(hd_txt,attrs=['bold'])
            print(header);print(dashes)
            
        ######################################################## END FEEDBACK ################################################################
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            
        ######################################################## ALGORITHM ###################################################################                                                                                                                                    
        #                                                                                                                                    #
        #                                                                                                                                    #
        #                                                                                                                                    #
        #                                                                                                                                    #
        ######################################################## START SIS ###################################################################
        g = self._start_network() ## initate the graph
        for i in range(self.n_iter):
            inf = self._find_by_attribute(g, "status", "I")  ## Infected Nodes ## find the total number of infected nodes
            sus = self._find_by_attribute(g, "status", "S")  ## Susceptible Nodes ## find the total number of susceptible nodes 
            ## For each infected node at time step t, we recover it with probability μ: 
            # we generate a uniform random number between 0.0 and 1.0, 
            possible_recoveries = np.random.uniform(0,1,len(inf)) ## << This is the probability that a node will recover FOR ALL THE NODES (thats why the len(inf) is used)

            # and if the value is lower than μ 
            # the state of that node in the next time step t+1 will be susceptible, otherwise it will remain being infected.
            ## apply array broadcasting to find the nodes that will recover ## possible_recoveries < MU returns True/False
            ## now if it is True and False, we "mask" the original "infected" array and only keep the True values (i.e. the nodes that will recover)
            inf2sus = inf[possible_recoveries < self.mu] ## infected to susceptible 
            inf2sus_idx = np.array([x.index for x in inf2sus]) ## get their index, because the above is a list of ig.Vertex objects

            ## susceptible to be infected 
            sus2inf = self._get_infected_neighbors(sus, self.beta) ## get the infected neighbors of the susceptible nodes ## more detail in the function itself
            sus2inf_idx = np.array([x.index for x in sus2inf]) ## getting the index 

            ## now we update the nodes
            ## update the infected nodes: inf2sus: I -> S
            self._update_nodes(g, inf2sus_idx, "S") ## update the status ## from the infected a small % will become S 
            ## update the infected nodes: sus2inf: S -> I
            self._update_nodes(g, sus2inf_idx, "I") ## update the color ## from the Susceptible a larger % will become I 
            ## get the infection rate 
            infection_rate = len(self._find_by_attribute(g, "status", "I")) / len(g.vs) ## (INFECTED / TOTAL_NODES)
            self.inf_rate[i] = infection_rate

            ############################################ MORE DETAILED FEEDBACK #############################################################
            if self.verbose:
                ## setting the texts
                it_txt = colored(f"{i+1}",attrs=['bold']) ## iteration
                inf_txt = colored(f"{len(inf)} ({len(inf)/self.N*100:.2f}%)",'red') ## INFECTED 
                sus_txt = colored(f"{len(sus)} ({len(sus)/self.N*100:.2f}%)",'green') ## SUSCEPTIBLE
                s2i_txt = colored(f"{len(sus2inf_idx)} ({len(sus2inf_idx)/self.N:.2f}%)","red") ## SUSCEPTIBLE TO INFECTED
                i2s_txt = colored(f"{len(inf2sus)} ({len(inf2sus)/self.N:.2f}%)","green") ## INFECTED TO SUSCEPTIBLE
                ir_txt = colored(f"{infection_rate:.2f}",'blue') ## INFECTION RATE
                ## filling it in 
                header_id = f"|{it_txt:^24s} | {inf_txt:^24s} | {sus_txt:^24s} | {s2i_txt:^24s} | {i2s_txt:^24s} | {ir_txt:^24s} |" ## use :^24s to make it centered and 24 chars long
                ## print the summary statistics
                print(header_id);print(dashes)
        rho_avg = np.mean(self.inf_rate[-(int(self.n_iter-self.t_trans)):])
        return rho_avg

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
        
        
