#!/usr/bin/env python3

# Standard library dependencies
# =============================
import sys
import json
import random
import math

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
        if random.random() < 0.8:
            seeds.append(focus)
        seeds.extend([n for n in G[focus] if random.random() < 0.8])
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
    top_degree = [k[0] for k in sorted(degrees, key=lambda t: t[1], reverse=True)]

    TA_set = set(top_degree[:num_seeds])

    final_seeds = []
    for i in range(50):
        idx = 0
        seeds = []
        while len(seeds) < num_seeds:
            seeds.append(top_degree[idx])
            nbrs = list(set(G[top_degree[idx]]) - set(seeds))

            TA_intersect = set(nbrs) & TA_set
            n_nbrs = len(TA_intersect) + 1

            # n_nbrs = int(math.floor(len(G[top_degree[idx]]) / 2) + 1)
            seeds.extend(np.random.choice(nbrs, size=n_nbrs))
            seeds = seeds[:num_seeds]
            idx += 1
        final_seeds.extend(seeds)
    print(len(final_seeds))
    with open(sys.argv[2], 'w') as fh:
        fh.write('\n'.join(final_seeds))

def look_around_you(adj_list, num_seeds, n_players):
    G = parse_graph(adj_list)
    degrees = G.degree()
    top_degree = [k[0] for k in sorted(degrees, key=lambda t: t[1], reverse=True)]

    TA_set = set(top_degree[:num_seeds])
    reach = dict()
    for TA_seed in TA_set:
        reach = update_reach(G, reach, TA_seed)
    
    taken = TA_set
    our_choices = list()
    for i in range(num_seeds):
        new_node = highest_value_node(G, reach)
        reach = update_reach(G, reach, new_node)
        our_choices.append(new_node)
    with open(sys.argv[2], 'w') as fh:
        fh.write('\n'.join(our_choices))

def highest_value_node(G, reach):
    max_val = -1
    max_node = None
    for node in G.nodes():
        new_val = node_value(G, reach, node)
        if new_val > max_val:
            max_val = new_val
            max_node = node
    return max_node
    
def update_reach(G, reach, newnode):
    new_reach = G.shortest_path_length(source = newnode)
    for node in new_reach:
        reach[node] = min(reach[node], new_reac[node])
    return reach

def node_value(G, reach, node):
    new_reach = G.shortest_path_length(source = node)
    result = 0
    for node in new_reach:
        if(reach[node] > new_reach[node]):
            result += 1
    return result



if __name__ == '__main__':
    try:
        with open(sys.argv[1], 'r') as fh:
            adj_list = json.loads(fh.read())
        look_around_you(adj_list, int(sys.argv[3]), int(sys.argv[4]))
    except IndexError as e:
        print('FEED ME A GRAPH')
        print('     (ಠ‿ಠ)     ')
