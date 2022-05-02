import numpy as np 
from .helpers import make_combinations

def main_config():
    VERBOSITY = False             ## Print the information about the steps, high verbosity. 
    SEED = 4234                   ## seed for the random number generator
    ## ------- ------- ------- -------
    ## -------  SIS PARAMETERS -------
    ## ------- ------- ------- -------
    P = 0.2                       ## initial infected population 
    MU = 0.1                      ## mu: spontaneous recovery probability 
    BETA = 0.02                   ## beta: infection probability, when S in contact with I (Transmission Rate)
    N = 500                       ## we will also need an initial population
    TIME_STEPS = 10                  ## time step
    PERCENTAGE = 0.9              ## Percentage tobe used as T_Trans
    T_TRANS = int(TIME_STEPS - TIME_STEPS*PERCENTAGE)
    N_REPS = 1                    ## number of repetitions for the simulation

    ## ------- ------- ------- -------
    ## -------  SIS DICTIONARY -------
    ## ------- ------- ------- -------
    MC_SIS_CONFIG = {
                "g":None,
                "initial_population":N,
                "initial_infected_population":P,
                "mu":MU,
                "beta":BETA,
                "n_iter":TIME_STEPS,
                "t_trans":T_TRANS,
                "seed":SEED,
                "verbose":VERBOSITY,
                }
    COMBS = make_combinations(mus = [0.1, 0.5, 0.9], betas = np.arange(0.00,1.02,0.02), verbosity = VERBOSITY)
    return MC_SIS_CONFIG, N_REPS, COMBS