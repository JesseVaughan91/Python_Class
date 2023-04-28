import requests
import json
import time
from datetime import datetime, timedelta
import time
from itertools import permutations
from itertools import combinations
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import networkx as nx
from networkx.classes.function import path_weight

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame

#authentication and connection details
api_key = 'PK3DNN23F6N5H8AI1Q80'
api_secret = 'uTFzXipeWGcf73SOPtKTVARYaAcp4U2nDpl0RKfd'
base_url = 'https://paper-api.alpaca.markets'

#instantiate Rest API
api = tradeapi.REST(api_key, api_secret, base_url, api_version = 'v2')

#lists of coin names and tickers to use in the api
coins = ['bitcoin-cash', 'litecoin', 'ethereum', 'bitcoin', 'tether', 'dogecoin', 'uniswap', 'solana', 'chainlink', 'dai']
tickers = ['bch', 'ltc', 'eth', 'btc', 'usdt', 'doge', 'uni', 'sol', 'link', 'dai']

#link indexes the coin and ticker lists to piece together the web api url
url = 'https://api.coingecko.com/api/v3/simple/price?ids='+ coins[0] + "," + coins[1] + "," + coins[2] + "," + coins[3] + "," + coins[4] + "," + coins[5] + "," + coins[6] + "," + coins[7] + "," + coins[8] + "," + coins[9] + '&vs_currencies='+ tickers[0] + "," + tickers[1] + "," + tickers[2] + "," + tickers[3] + "," + tickers[4] + "," + tickers[5] + "," + tickers[6] + "," + tickers[7] + "," + tickers[8] + "," + tickers[9]

#Load the json files in order to conduct analysis
request = requests.get(url)
data = json.loads(request.text)

#Save data to json file
with open("/home/ubuntu/environment/final_project/data/crypto_data.json", "w") as f:
    json.dump(data, f)

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
            continue
            # print("Can't trade between these coins")

#Makes all the edges from the edges list weighted from the nx library DiGraph that was defined previously
g.add_weighted_edges_from(edges)
#lists and dictionaries initialized in order to track the greatest and smallest paths later.
greatest_weight = -99999999
greatest_path = []
lowest_weight = 99999999
lowest_path = []
# create a txt file to output all data to. Instead of printing data, save to txt file.
currency_combinations = open('/home/ubuntu/environment/final_project/currency_combinations.txt', 'w')
# loop to iterate through each of the combinations of nodes.
for n1, n2 in combinations(g.nodes, 2):
    print("paths from ", n1, "to", n2, "------------------------------------", file = currency_combinations)
    #nx.all_simple_paths is used to draw the path between the to and from nodes (source & target)
    for path in nx.all_simple_paths(g, source = n1, target = n2):
        path_weight_to = 1
        #loop used to calculate the weighted average of the edges by multiplying the path weights.
        for i in range(len(path)-1):
            path_weight_to *= g[path[i]][path[i + 1]]["weight"]
        print(path, path_weight_to, file = currency_combinations)
    
        #paths are reversed to complete the check for disequilibrium.
        path.reverse()
        
        path_weight_from = 1
        #loop used to calculate the weighted average of the edges by multiplying the path weights.
        for i in range(len(path)-1):
            path_weight_from *= g[path[i]][path[i + 1]]["weight"]
        print(path, path_weight_from, file = currency_combinations)
        #calculation for the path weight factor. the to and from path weights are multiplied.
        path_weight_factor = path_weight_to * path_weight_from
        #overall path weight is printed.
        print(path_weight_factor, file = currency_combinations)
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
print("Smallest path weight factor: ", lowest_weight)
print("Paths: ", lowest_path, lowest_path[::-1])
print("Greatest path weight factor: ", greatest_weight)
print("Paths: ", greatest_path, greatest_path[::-1])
print()

# save picture of arbitrage paths.
pos=nx.circular_layout(g)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
plt.savefig("arbitrage.png")


print("--------------------------------------")
# The following statement will run if the greatest path weight factor is greater than 1 (Disequalebrium)
if greatest_weight > 1:
    print("The following coins will be purchased in this order: ", greatest_path, "\n")
    # Iterate through each ticker in the greatest path list.
    for i in greatest_path:
        # Convert the coingecko compatable ticker names to names that work with Alpaca
        tick = i.upper() + "/USD"
        # purchase order for each coin based on the tick variable
        api.submit_order(symbol = tick,
        notional = '500',
        side = 'buy',
        type = 'market',
        time_in_force = 'gtc')
        print("Purchased $500 of ", i)
        
        # time delay is used to provide time for the purchase orders to be placed
        time.sleep(5)

        #sell the previously purchased coin.
        api.submit_order(symbol = tick,
        notional = '400',
        side = 'sell',
        type = 'market',
        time_in_force = 'gtc')
        print("Sold $400 of ", i)
        print()
    print("--------------------------------------")
    
    # reverse the greatest path list to purchase the coins in reverse order to take advantage of the disequalibrium
    greatest_path.reverse()
    print("In order to complete the arbitrage, the coins will be purchased in reverse order: ", greatest_path, "\n")
    # The steps below are the same as the previous for loop but are conducted in reverse order now.
    for i in greatest_path[1:]:
        tick_reverse = i.upper() + "/USD"
        
        time.sleep(5)
        # submit purchase order for coin
        api.submit_order(symbol = tick_reverse,
        notional = '500',
        side = 'buy',
        type = 'market',
        time_in_force = 'gtc')
        print("Purchased $500 of ", i)
        
        time.sleep(5)
        #sell previously purchased coin
        api.submit_order(symbol = tick_reverse,
        notional = '400',
        side = 'sell',
        type = 'market',
        time_in_force = 'gtc')
        print("Sold $400 of ", i)
        print()
