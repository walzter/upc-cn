# file handling
import os
import glob
import zipfile
# file types and typing
from collections import defaultdict
from typing import List, DefaultDict
# graphs
import igraph
import igraph as ig
# plotting 
import matplotlib.pyplot as plt
# dataframe & linalg
import pandas as pd
import numpy as np

# plotting parameters 
plt.rcParams.update({"font.size": 25})

def extract_zip(data_dir:os.path, output_dir:os.path) -> None:
    """Extracts zip-files to current working directory"""
    ## check if output_dir exists else create it 
    if not os.path.exists(output_dir):
        ## reading & extracting zip file 
        with zipfile.ZipFile(data_dir, "r") as file:
                file.extractall()
    else: print("Folder already exists")

def read_net_files(dir_path:os.path, verbosity:bool =True) -> DefaultDict[str, DefaultDict[str, List[igraph.Graph]]]:
    """Read zipfile and load .net file into memory"""
    
    ## all the .net files 
    path_files = glob.glob(dir_path + "/*/*.net", recursive=True)
    
    ## getting their category (toy, model, real) and file_path 
    # category 
    category = [x.split('/')[-2] for x in path_files]
    
    # name of the graph
    graph_names = [x.split('/')[-1] for x in path_files]
    
    # loaded_graphs
    loaded_graphs = [ig.read(x) for x in path_files]
    
    # create the tuple 
    data_tuple = list(zip(category, graph_names, loaded_graphs))
    
    # dictionary to store the results 
    data_dict = defaultdict(lambda: defaultdict(list))
    
    # update the dictionary with the values 
    _ = [data_dict[a][b].append(c) for a,b,c in data_tuple]
    
    if verbosity:
        ## number of datasets 
        print(f"There are {len(data_dict.keys())} datasets in the directory: {dir_path}") 
        ## number of graphs per dataset
        for k,v in data_dict.items():
            print(f"-->{k.upper()}<-- Dataset contains {len(v)} files / graphs")
    return data_dict
    
    
    
"""

Replaced with the two functions above: 

- extract_zip 

- read_net_files 

Reasoning to make two functions: 
    1. Coupling is bad -> a function should serve one single purpose 
    2. read_net_files -> returns a dictionary, faster  

def read_data(dir_path:os.path, verbosity:bool = True):
    "

    This function read the path and deliver lists, one of them, with the name of the kind of model graph names
    and the other with the graphs.

    PARAMS:
    ------
    dir_path : Path of folder with data 
    
    RETURNS:
    --------
    data_networks : List[igraph.graph]


    "
    ## list files in directory 
    name_networks = os.listdir(dir_path)
    
    ## some feedback
    
    root_networks = glob.glob(dir_path + "/*.net")
    data_networks = []
    for i in range(len(root_networks)):
        data_networks.append(igraph.read(root_networks[i]))
        print(name_networks[i])
    return data_networks, name_networks
"""

def compute_descriptors(name, graphs):
    """
    This function takes the name and graphs models and calculates the descriptors, then stores them in a csv file
    :param name:    Neural network type name

    :param graphs:  Neural network file graphs

    :return:        Number of nodes
                    Number of edges
                    Minimum, maximum, and average degree
                    Average clustering coefficient (average of the clustering coefficient of each node)
                    Assortativity
                    Average path length (average distance between all pairs of nodes)
                    Diameter (maximum distance between nodes in the network)
    """

    descriptors = []
    number_files = len(graphs)
    for i in range(number_files):
        number_models = len(graphs[i])

        for j in range(number_models):
            Model_name = name[i][j]
            nodes = graphs[i][j].vcount()
            edges = graphs[i][j].ecount()
            average_degree = "{:.4f}".format(
                float(edges / nodes)
            )  # Total Edges/Total Nodes=Average Degree
            max_degree = graphs[i][j].maxdegree()
            min_degree = min(graphs[i][j].degree())
            avg_clustering_cf = "{:.4f}".format(
                float(graphs[i][j].transitivity_undirected())
            )
            assortat = "{:.4f}".format(float(graphs[i][j].assortativity_degree()))
            avg_path_length = "{:.4f}".format(
                float(np.mean(graphs[i][j].shortest_paths()))
            )
            diameter = graphs[i][j].diameter()
            descriptors.append(
                [
                    Model_name,
                    nodes,
                    edges,
                    average_degree,
                    max_degree,
                    min_degree,
                    avg_clustering_cf,
                    assortat,
                    avg_path_length,
                    diameter,
                ]
            )
    descriptors = pd.DataFrame(descriptors)
    descriptors.columns = [
        "Model",
        "Nodes",
        "Edges",
        "Average_degree",
        "Max_degree",
        "Min_degree",
        "Average_clustering_coefficient",
        "Assortativity",
        "Average_path_length",
        "Diameter",
    ]
    print(descriptors)
    return descriptors


def real_networks_airports(name, networks):
    """

    Numerical descriptors of the nodes of the network real/airports_UW.net


    :param name:
    :param networks:
    :return:
                        1.Degree *
                        2.Strength*
                        3.Clustering coefficient - NO SE SI ESTA BIEN
                        4.Average path length (average distance to the rest of the nodes)*
                        5.Maximum path length (maximum distance to the rest of the nodes)*
                        6.Betweenness*
                        7.Eigenvector centrality -FALTA ESCOGER SOLO LOS VALORES DE LOS AEROPUERTOS
                        8.PageRank*
    """
    airports = [
        "PAR",
        "LON",
        "FRA",
        "AMS",
        "MOW",
        "NYC",
        "ATL",
        "BCN",
        "WAW",
        "CHC",
        "DJE",
        "ADA",
        "AGU",
        "TBO",
        "ZVA",
    ]
    name_networks = name[2][2]
    graph_networks = networks[2][2]

    descriptors = []
    Average_path_length = []
    Maximum_path_length = []
    """1.Degree *"""
    degree = graph_networks.degree(airports)
    """2.Strength*"""
    strength = graph_networks.strength(airports)
    """3.Clustering coefficient - NO SE SI ESTA BIEN"""
    clustering = graph_networks.transitivity_undirected()
    print("El clustering pero en general, toca arreglar esto")
    print(clustering)

    for i in range(len(airports)):
        """4.Average path length (average distance to the rest of the nodes)*"""
        Average_path_length.append(
            "{:.8f}".format(np.mean(graph_networks.shortest_paths(airports[i])))
        )
        # Average_path_length.append(graph_networks.get_shortest_paths(airports[i]))
        """5.Maximum path length (maximum distance to the rest of the nodes)*"""
        Maximum_path_length.append(np.max(graph_networks.shortest_paths(airports[i])))

    """6.Betweenness*
    The betweenness centrality for each vertex is the number
     of these shortest paths that pass through the vertex."""
    betweenness = graph_networks.betweenness(
        airports, directed=False
    )  # Revisar pq no estoy seguro

    """7.Eigenvector centrality -FALTA ESCOGER SOLO LOS VALORES DE LOS AEROPUERTOS"""
    eigen_vector_cent = graph_networks.eigenvector_centrality()
    print(
        "EL eigen vector me salen todos pero necesitamos solo quedarnos con los de la lista"
    )
    print(len(eigen_vector_cent), eigen_vector_cent)
    """8.PageRank*"""
    page_rank = graph_networks.pagerank(airports)
    """We put all the descriptors computed in a list and them, we convert it in a dataframe"""
    descriptors = [
        airports,
        degree,
        strength,
        Average_path_length,
        Maximum_path_length,
        betweenness,
        page_rank,
    ]

    Airport_descriptors = pd.DataFrame(descriptors)
    Airport_descriptors = Airport_descriptors.T
    Airport_descriptors.columns = [
        "Airport_name",
        "Degree",
        "Strength",
        "Average path length",
        "Maximum path length",
        "Betweenness",
        "Page rank",
    ]
    Airport_descriptors.to_csv("./results/Airports_Descriptors.csv", index=True)
    # print(Airport_descriptors)

    # ver_network(graph_networks)


def ver_network(graph):

    """
    THis function is used to plot the graph model
    :param graph: graph model
    :return: An image with the plot graph model and its conections
    """
    out_fig_name = graph + ".eps"
    visual_style = {}
    # Define colors used for outdegree visualization
    colours = ["#fecc5c", "#a31a1c"]

    # Set bbox and margin
    visual_style["bbox"] = (3000, 3000)
    visual_style["margin"] = 17

    # Set vertex colours
    visual_style["vertex_color"] = "grey"

    # Set vertex size
    visual_style["vertex_size"] = 20

    # Set vertex lable size
    visual_style["vertex_label_size"] = 8

    # Don't curve the edges
    visual_style["edge_curved"] = False

    # Set the layout
    my_layout = graph.layout_fruchterman_reingold()
    visual_style["layout"] = my_layout

    # Plot the graph
    # ig.plot(graph, out_fig_name, **visual_style)
    ig.plot(
        graph,
        layout=my_layout,
        vertex_size=5,
        vertex_color=["blue", "red", "green", "yellow"],
        vertex_label=["f", "s", "t", "f"],
        edge_width=[1, 5],
        edge_color=["black", "grey"],
        edge_curve=True,
    )
