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
import seaborn as sns
# dataframe & linalg
import pandas as pd
#import pickle
import numpy as np
import gc 
# progress bar 
from tqdm import tqdm
## utils 
from utils.numerical_descriptors import NumericalNetworkDescriptor
from utils.airport_descriptors import AirportDescriptor

# plotting parameters 
#plt.rcParams.update({"font.size": 25})

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
    
###
def extract_data_and_save(model_dictionary:dict, output_name:str, save_csv:bool=True) -> None:
    """writes data from model dictionary to csv"""
    holder = []

    # iterate through dictionary 
    for k, v in model_dictionary.items():
        ## get the models 
        for models in v: 
            ## define the data 
            data = NumericalNetworkDescriptor(dataset=k,
                                            file_name=models,
                                            loaded_graph=model_dictionary[k][models])
            holder.append(data._summary())
            gc.collect()
    # data frame 
    df = pd.DataFrame(holder)
    ## save 
    if save_csv:
        df.to_csv(f"./results/{output_name}.csv")
    return df


## 
def extract_airport_descriptors(graph:igraph.Graph, file_name:str,airport_list:list, rounding_value:int=8,save_csv=True) -> None:
    """Extracts the Descriptors for the specified graph -> Airport in this case"""
    ## pass it through our AirportDescriptor class 
    air_port = AirportDescriptor(graph)
    ## Rounding datframe to 8 decimals 
    df = pd.DataFrame(air_port._summary())
    df = df.round(rounding_value)
    if save_csv: 
        df.to_csv(f"./results/{file_name}.csv")
    if airport_list is not None: 
        df_report = df.loc[df['Airport'].isin(airport_list)]
        df_report = df_report.round(rounding_value)
        df_report.to_csv("./results/{file_name}_REPORT_15_AIRPORTS.csv")
    return air_port

def plot_linear_log_histogram(graph_bins:list, number_bins:int, graph_name:str) -> None:
    """Plots the Linear and the Log Histogram"""
    # histogram on linear scale
    plt.subplot(121)
    #fig, axs = plt.subplots(1,2,figsize=figure_size)
    hist, bins, _ = plt.hist(graph_bins, bins=number_bins)
    #axs[0].hist(graph_bins, bins=number_bins)
    plt.title(f"Linear plot for {graph_name}")

    # histogram on log scale. 
    # Use non-equal bin sizes, such that they look equal on log scale.
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    plt.subplot(122)
    plt.hist(graph_bins, bins=logbins)
    plt.xscale('log')
    plt.title(f"Log-Log plot for {graph_name}")
    # save the figure 
    plt.savefig(f'./images/PDF/FIGURE_{graph_name}')
    plt.tight_layout()
    plt.show()



def plot_ccdf(graph_bins:list, number_bins:int, graph_name:str):
    """Plots the CCDF of the given bins from the graph distribution"""
    ## plotting 
    plt.hist(graph_bins, bins=number_bins, density=True, histtype='step', linewidth=3,cumulative=-1, label='Empirical')
    plt.title(f'CCDF for the graph {graph_name}')
    plt.xlabel('Number of Edges')
    plt.xlim(0,50)

    plt.xticks(range(0,50,5))
    plt.grid(True)
    plt.ylabel('Percentage of Nodes ')
    plt.yticks(np.arange(0,1.0,0.1))
    plt.savefig('./images/CCDF/FIGURE_{graph_name}')
    plt.show()
    plt.clf()
    


def make_histograms_pdf(bins:int):
    """Plots and saves the histograms (PDF) of the given networks to plot"""

    ## networks to graph 
    networks_to_graph = [
                    "./A1-networks/model/ER5000k8.net",
                    "./A1-networks/model/SF_1000_g2.7.net",
                    "./A1-networks/model/ws1000.net",
                    "./A1-networks/real/airports_UW.net",
                    "./A1-networks/real/PGP.net"
                    ]
    
    ## reading the graphs 
    loaded_graphs = [igraph.read(x) for x in networks_to_graph]

    ## degrees for each 
    degrees_per_graph = [x.degree_distribution()._bins for x in loaded_graphs]
    ## names
    names = [x.split("/")[-1].replace(".","_") for x in networks_to_graph]
    # making a dictionary
    d = dict(zip(names, degrees_per_graph))
    
    # plotting
    for k, v in d.items():
        plot_linear_log_histogram(graph_bins=v,
                                    number_bins=bins,
                                    graph_name=k)
    
    ## plot CCDF 
        plot_ccdf(graph_bins=v,
                number_bins=20,
                graph_name=k)
        
"""
Maybe increase efficiency with multithreading ?

Yes multithreading pool can work !!

"""
def get_average_max_len(graph:igraph.Graph, node:int) -> float:
    """ gets all the paths and gets averag and max"""
    ## all the path lengths
    path_len = [len(p) for p in graph.get_all_shortest_paths(v=node)]
    ## average path 
    avg_path = round(np.mean(path_len), 8)
    ## max 
    max_path = round(np.max(path_len), 8)
    
    return avg_path, max_path 




def extract_avg_max_len(graph: igraph.Graph) -> dict:
    """Function which iterates over the graph and extracts the avg and max length for each node."""
    d = dict()
    for _, node in enumerate(tqdm(graph.vs())):
        ## id of the node 
        node_id,node_name = node['id'], node['name']
        #print(node_name)
        ## get the distance 
        avg_len, max_len = get_average_max_len(graph, node=node_id)
        d[node_name] = {
                        "avg_len": avg_len,
                        "max_len": max_len
                        }
        gc.collect()
    return d