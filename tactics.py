#!/usr/bin/env python3

# Standard library dependencies
# =============================
import sys
import json
import random

# Local dependencies
import sim

# Third-party dependencies
# ========================
import networkx as nx
import numpy as np

def parse_graph(adj_list):
    G = nx.Graph()
    for key in adj_list.keys():
        G.add_edges_from([(key, val) for val in adj_list[key]])
    return G

def selector(G,num_seeds,best_boys):

    #input variables: bestboys, G, num_seeds
    focus = best_boys[0][0]
    i=1
    seeds = []
    while len(seeds) < num_seeds:
        if random.random() < 1: #0.8:
            seeds.append(focus)
        seeds.extend([n for n in G[focus] if random.random() < 1])
        seeds = seeds[:num_seeds]
        focus = best_boys[i][0]
        i += 1
    return seeds


def tactics_1st_gen(adj_list, num_seeds, n_players):
    N = 100
    G = parse_graph(adj_list)
    print('Total number of nodes: {}'.format(G.number_of_nodes()))
    centrality = nx.eigenvector_centrality(G)
    central_nodes = [k for k in sorted(centrality, key=centrality.get, reverse=True)]
    print('most central: {}'.format(','.join([central_nodes[i] for i in range(10)])))


    clustering = nx.clustering(G, central_nodes[:N])
    cluster_nodes = [k for k in sorted(clustering, key=clustering.get, reverse=True)]
    print('highest clustering coefficient: {}'.format(','.join([cluster_nodes[i] for i in range(10)])))

    best_boys = [(n, centrality[n] * clustering[n]) for n in central_nodes[:N]]
    best_boys = sorted(best_boys, key=lambda t: t[1], reverse=True)

    final_selections = []
    for i in range(50):
        selections = dict((str(i), selector(G, num_seeds, best_boys[i:])) for i in range(n_players))
        simulation = sim.run(adj_list, selections)
        best = [k for k in sorted(simulation, key=simulation.get, reverse=True)][0]
        final_selections.extend(selections[best])
    print(final_selections)
    print(len(final_selections))
    with open(sys.argv[2], 'w') as fh:
        fh.write('\n'.join(final_selections))

def tactics_2nd_gen(adj_list, num_seeds, n_players):
    G = parse_graph(adj_list)
    degrees = G.degree()
    print(degrees)
    print(G.degree(['1']))
    top_degree = [k for k in sorted(degree, key=lambda t: t[1], reverse=True)]


if __name__ == '__main__':
    try:
        with open(sys.argv[1], 'r') as fh:
            adj_list = json.loads(fh.read())
        tactics_1st_gen(adj_list, int(sys.argv[3]), int(sys.argv[4]))
    except IndexError as e:
        print('FEED ME A GRAPH')
        print('     (ಠ‿ಠ)     ')
