"""Structural descriptors of complex networks"""
"""Authors: Edison Bejarano - Eric Walzthöny"""

## Import Scripts 
from utils.utils import extract_zip, read_net_files
from utils.utils import extract_data_and_save
from utils.utils import extract_airport_descriptors
from utils.utils import make_histograms_pdf
import gc 
def main(ZIP_PATH:str, OUTPUT:str) -> None: 
    """Main function to run the functions"""
    ## Extract the zipfile, if the output dir exists it will skip
    print("Extracting zip file...\n")
    extract_zip(ZIP_PATH, OUTPUT)

    ## Reading all the pajek files (.net files)
    print("Loading Pajek files into memory...\n")
    net_files = read_net_files(OUTPUT, verbosity=True)

    ##### Part A: Numerical Descriptors of Networks ######
    ## extract the data and optionally save the CSV
    print("Initializing Numerical Descriptor Extraction of Pajek files...\n")
    df = extract_data_and_save(net_files, "new_Descriptors", save_csv=True)
    ## verbosity 
    print("Succesfully saved the Numerical Descriptors\n")

    ## sanity 
    gc.collect()

    ##### Part B: Numerical Descriptors of Real Network - AIRPORT ######
    ## get the airport file from memory 
    print("Initializing the Airport Numerical Description Extraction....\n")
    airport = net_files['real']['airports_UW.net'][0]
    ## For the report 
    airport_to_calculate = [
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

    ## extract the airport descriptors
    air_port = extract_airport_descriptors(graph = airport, 
                                        file_name = "NEW_Airport_Descriptor",
                                        airport_list=airport_to_calculate,
                                        save_csv = True)
    print("The Airport Numerical Descriptors were extracted correctly! \n")
    
    ## sanity 
    gc.collect()

    ### PART C: Histograms and CCDF
    make_histograms_pdf(bins=15)

if __name__ == "__main__":
    ## Variable configuration
    ## Path to the zip file 
    ZIP_PATH = './A1-networks.zip'
    ## extracted directory
    OUTPUT = './A1-networks/'    
    main(ZIP_PATH, OUTPUT)