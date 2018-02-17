#!/usr/bin/env python3

# Standard library dependencies
# =============================
import sys
import json

# Local dependencies
import sim

# Third-party dependencies
# ========================
import networkx as nx
import numpy as np
import random

def parse_graph(adj_list):
    G = nx.Graph()
    for key in adj_list.keys():
        G.add_edges_from([(key, val) for val in adj_list[key]])
    return G

def selector(G,num_seeds,best_boys):

    #input variables: bestboys, G, num_seeds
    num_seeds-=1
    focus=best_boys[0][0]
    i=1
    while num_seeds > len(G[focus]):
        focus=best_boys[i][0]
        i+=1
        
    seeds=[focus]
    indices=random.sample(range(len(G[focus])), num_seeds) #pick at random
    
    for index in indices:
        seeds.append(list(nx.all_neighbors(G, focus))[index])
        
    return seeds


def tactics(adj_list,num_seeds):
    G = parse_graph(adj_list)
    print('Total number of nodes: {}'.format(G.number_of_nodes()))
    centrality = nx.eigenvector_centrality(G)
    central_nodes = [k for k in sorted(centrality, key=centrality.get, reverse=True)]
    print('most central: {}'.format(','.join([central_nodes[i] for i in range(10)])))


    clustering = nx.clustering(G, central_nodes[:10])
    cluster_nodes = [k for k in sorted(clustering, key=clustering.get, reverse=True)]
    print('highest clustering coefficient: {}'.format(','.join([cluster_nodes[i] for i in range(10)])))

    best_boys = [(n, centrality[n] * clustering[n]) for n in central_nodes[:10]]
    best_boys = sorted(best_boys, key=lambda t: t[1], reverse=True)
    print(best_boys)
    
    seeds=selector(G,num_seeds,best_boys)
    print()
    print(seeds)
    print()

def simulate(adj_list, best_boys, seeds):
    pass



if __name__ == '__main__':
    try:
        with open(sys.argv[1], 'r') as fh:
            adj_list = json.loads(fh.read())
        tactics(adj_list,int(sys.argv[2]))
    except IndexError as e:
        print('FEED ME A GRAPH')
        print('     (ಠ‿ಠ)     ')
