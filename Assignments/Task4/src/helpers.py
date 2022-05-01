import itertools
def make_combinations(mus:list, betas:list, verbosity:bool):
    combs = list(itertools.product(mus,betas)) ## make a combination of all the mus and betas
    if verbosity: 
        print(f"Number of Mu values: {len(mus)} | Number of Beta values: {len(betas)} | Total combinations: {len(COMBS)}")
    return combs