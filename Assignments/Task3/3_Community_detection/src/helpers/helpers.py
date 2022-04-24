import glob
import networkx as nx 

## define the function to load the files
def get_net_files(dir_to_files: str) -> list:
    """
    get the list of files in the directory
    """
    return glob.glob(dir_to_files + "*/*.net")


## define a function that matches the .net file with the corresponing .clu file
def get_clu_files(dir_to_files: list) -> dict:
    """
    Get the .clu files
    """
    ## get the list of files
    return glob.glob(dir_to_files + "*/*.clu")


## define function to iterate through a list of files and returns get_file_list
def get_file_dict(data_directory: str) -> dict:
    """
    get the list of files in the directory and store them as a dictionary
    d = {'model_type': file_list}
    """
    ## get the list of files
    ## networks
    list_of_nets = get_net_files(data_directory)
    list_of_clus = get_clu_files(data_directory)
    ## find the corresponding .clu file
    net_clu_pairs = [
        (file, clu)
        for file in list_of_nets
        for clu in list_of_clus
        if file.split("/")[-1].split(".")[0] in clu.split("/")[-1]
    ]
    ## import collections defaultdict
    from collections import defaultdict

    net_clu_dict = defaultdict(list)
    _ = [
        net_clu_dict[x[0].split("/")[2].upper()].append(net_clu_pairs[idx])
        for idx, x in enumerate(net_clu_pairs)
    ]
    ## dictionaries
    return net_clu_dict


## reading the clu file
def read_clu(file_path: str) -> list:
    """
    Read the .clu file and return the list of communities.
    """
    with open(file_path, "r") as f:
        return [
            (idx, int(line.strip()))
            for idx, line in enumerate(f.readlines())
            if line[0] != "*"
        ]


##
def replace_text_edges(partition: list, mapper: dict) -> list:
    """Replaces the text in a list of lists with the corresponding integer"""
    ll = []
    for p in partition:
        if len(p) == 1:
            new_val = mapper[p[0]]
            ll.append(new_val)
        elif len(p) > 1:
            l = []
            for i in p:
                l.append(mapper[i])
            ll.append(l)
    return ll


def lol2idx(lol: list) -> list:
    """
    Convert a list of lists to a list of indexers
    """
    d = dict()
    _ = [d.setdefault(val, idx) for idx, sublist in enumerate(lol) for val in sublist]
    return d


def dict_vals_to_list(d: dict) -> list:
    """
    Convert a dictionary to a list of values
    """
    return list(d.values())

def load_graph_coords(graph: nx.Graph) -> tuple:
    net = nx.read_pajek(graph)
    try:
        coord_x = net.vs['x']
        coord_y = net.vs['y']
        pos = [(coord_x[i], coord_y[i]) for i in range(len(coord_x))]
    except:
        pos=nx.kamada_kawai_layout(net)
    return (net, pos)