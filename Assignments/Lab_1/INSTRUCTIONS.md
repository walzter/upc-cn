A1. Structural descriptors of complex networks
Calculation of structural descriptors of complex networks

The attached file "A1-networks.zip" contains several undirected complex networks in Pajek format (*.net), grouped in three categories: toy (sample networks), model (networks generated from models), and real (real networks). The objective is the calculation of the main structural descriptors for all the provided networks. More precisely, you have to calculate at least:

a) Numerical descriptors of networks [Done]

Number of nodes [Done]
Number of edges [Done]
Minimum, maximum, and average degree [Done]
Average clustering coefficient (average of the clustering coefficient of each node) [Done]
Assortativity [Done]
Average path length (average distance between all pairs of nodes) [Done]
Diameter (maximum distance between nodes in the network) [Done]

Use 4 decimal digits for the non-integer descriptors. Put the results in table form for all the networks in the A1-networks.zip file.



b) Numerical descriptors of the nodes of the network real/airports_UW.net

Degree
Strength
Clustering coefficient
Average path length (average distance to the rest of the nodes)
Maximum path length (maximum distance to the rest of the nodes)
Betweenness
Eigenvector centrality
PageRank
Use 8 decimal digits for the non-integer descriptors. Except for the strength, always consider the network as unweighted. Put the results for all the nodes in a CSV or Tab-separated file. Add to the document a table including the descriptors corresponding to the following airports:

PAR, LON, FRA, AMS, MOW, NYC, ATL, BCN, WAW, CHC, DJE, ADA, AGU, TBO, ZVA

c) Plot the histograms of the degree distributions (PDF, probability distribution function) and the complementary cumulative degree distributions (CCDF) for the following networks:

model/ER5000k8.net
model/SF_1000_g2.7.net
model/ws1000.net
real/airports_UW.net
real/PGP.net
For each network, choose the appropriate histogram form, either linear or log-log histogram. If both histograms are included, then specify explicitly which one is the appropriate one. The number of bins of the histograms must be between 10 and 30.

Note we are asking for the CCDF, not the CDF, and that all plots in c) must be histograms.

Alternatively, you may implement yourself the calculation of (some of) the descriptors.

## The delivery must include:

Document in PDF with all the results:
Description of how you have done both parts (software, decisions, etc.)

Table of network descriptors as described in a)
Table of selected nodes descriptors as described in b)

Histograms of the PDF and CCDF of the degree distributions, selecting the proper type (either linear or log-log) as described in c)

Source code

Results files (not the networks, only the results)
