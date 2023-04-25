import requests
import json
import time
from datetime import datetime, timedelta
from itertools import permutations
from itertools import combinations

import os
# os.system("sudo pip3 install networkx")
# os.system("sudo apt-get update")
# os.system("sudo apt-get install libjpeg-dev zlib1g-dev")
# os.system("sudo -H pip3 install Pillow")
# os.system("sudo -H pip3 install matplotlib")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import networkx as nx
from networkx.classes.function import path_weight

#lists of coin names and tickers to use in the api
coins = ['ripple', 'cardano', 'bitcoin-cash', 'eos', 'litecoin', 'ethereum', 'bitcoin']
tickers = ['xrp', 'ada', 'bch', 'eos', 'ltc', 'eth', 'btc']

#link indexes the coin and ticker lists to piece together the web api url
url = 'https://api.coingecko.com/api/v3/simple/price?ids='+ coins[0] + "," + coins[1] + "," + coins[2] + "," + coins[3] + "," + coins[4] + "," + coins[5] + "," + coins[6] + '&vs_currencies='+ tickers[0] + "," + tickers[1] + "," + tickers[2] + "," + tickers[3] + "," + tickers[4] + "," + tickers[5] + "," + tickers[6]

#Load the json files in order to conduct analysis
request = requests.get(url)
data = json.loads(request.text)


#Digraph is a directed graph used to show the edges and their direction between nodes
g =  nx.DiGraph()
edges = []

#for loop to iterate through the coins and tickers to identify the from coin and ticker
for i in range(len(coins)):
    from_coin = coins[i]
    from_ticker = tickers[i]
    
    #Loop to identify the to node's ticker
    for ticker in tickers:
        to_node = ticker
        
        #Checks to make sure tickers aren't going to each other (i.e. btc to btc)
        if from_ticker == to_node:
            continue
        #Weights are attempted here, but in the event that there is no data on coins
        #those coins are skipped (cardano)
        try:
        #the weight is identified throough indexing
        #the to and from tickers and the weights are appended to the edges list as tuples
            weight = data[from_coin][to_node]
            edges.append((from_ticker, to_node, weight))
        except:
            print("Can't trade between these coins")

#Makes all the edges from the edges list weighted from the nx library DiGraph that was defined previously
g.add_weighted_edges_from(edges)
#lists and dictionaries initialized in order to track the greatest and smallest paths later.
greatest_weight = -99999999
greatest_path = []
lowest_weight = 99999999
lowest_path = []
#loop to iterate through each of the combinations of nodes.
for n1, n2 in combinations(g.nodes, 2):
    print()
    print("paths from ", n1, "to", n2, "------------------------------------")
    #nx.all_simple_paths is used to draw the path between the to and from nodes (source & target)
    for path in nx.all_simple_paths(g, source = n1, target = n2):
        path_weight_to = 1
        #loop used to calculate the weighted average of the edges by multiplying the path weights.
        for i in range(len(path)-1):
            path_weight_to *= g[path[i]][path[i + 1]]["weight"]
        print(path, path_weight_to)
    
        #paths are reversed to complete the check for disequilibrium.
        path.reverse()
        
        path_weight_from = 1
        #loop used to calculate the weighted average of the edges by multiplying the path weights.
        for i in range(len(path)-1):
            path_weight_from *= g[path[i]][path[i + 1]]["weight"]
        print(path, path_weight_from)
        #calculation for the path weight factor. the to and from path weights are multiplied.
        path_weight_factor = path_weight_to * path_weight_from
        #overall path weight is printed.
        print(path_weight_factor)
    #checks if the path weight factor is greater than the initialized variable
    #if yes, update the value and change the value in the greatest value list.
    if path_weight_factor > greatest_weight:
        greatest_weight = path_weight_factor
        greatest_path = path
    #checks if the path weight factor is less than the initialized variable
    #if yes, update the value and change the value in the lowest value list.
    elif path_weight_factor < lowest_weight:
        lowest_weight = path_weight_factor
        lowest_path = path
#results are printed to the console to show the bst and worst arbitrage opportunities. 
print()
print("Smallest path weight factor: ", lowest_weight)
print("Paths: ", lowest_path, lowest_path[::-1])
print("Greatest path weight factor: ", greatest_weight)
print("Paths: ", greatest_path, lowest_path[::-1])

#The below code is used to create the graph of nodes and edges and then to save the results to a png file.
pos=nx.circular_layout(g)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
plt.savefig("arbitrage.png")
