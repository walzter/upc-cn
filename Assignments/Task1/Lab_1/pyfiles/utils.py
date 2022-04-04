# libs
import time
from glob import glob
from tqdm import tqdm
import pandas as pd
from pyfiles.numerical_descriptor import NumericalNetworkDescriptor


def make_df_time(path: str) -> pd.DataFrame:
    """ Outputs summary file for different pajek graph file formats. Also times it. 
    
    PARAMETERS:
    -----------
    
    path: str
          path to the folder which contains the .net files, which want to be summarized. 
    
    RETURNS:
    --------
    holder : pd.DataFrame
             returns the summary of the graphs in a pandas DataFrame. 
    
    """
    new_path = path + '/*.net'
    file_list = glob(new_path)
    holder = []
    gtic = time.time()
    for idx,graphs in enumerate(tqdm(file_list)):
        tic = time.time()
        tmp = NumericalNetworkDescriptor(graphs)
        holder.append(tmp._summary())
        toc = time.time()
        holder[idx]['Time'] = round((toc-tic), 4)
    gtoc = time.time()
    print(f"The elapsed time is: {gtoc-gtic:.4f}")
    return pd.DataFrame(holder)

# joining all the dataframes 
def join_csvs(path):
    """ Joins csv files in the specified folder 
    
    PARAMETERS:
    -----------
    
    path: str
          path to the folder which contains the .csv files, which want to be merged.
    
    RETURNS:
    --------
    df : pd.DataFrame
             returns the combined csv files in a pd.DataFrame
    
    """
    rel_path = f'{path}/*.csv'
    ls = glob(rel_path)
    df_ls = [pd.read_csv(x) for x in ls]
    df = pd.concat(df_ls)
    df = df.drop('Unnamed: 0', axis=1)
    df.to_csv('res/combined_data.csv') # optional 
    return df