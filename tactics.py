#!/usr/bin/env python3

# Standard library dependencies
# =============================
import sys
import json
import random
import math

# Local dependencies
import sim
from look_around_you import look_around_you

# Third-party dependencies
# ========================
import networkx as nx
import numpy as np

def print_to_file(seeds, filename):
    print('Printing {} lines to file {}'.format(len(seeds), filename))
    with open(filename, 'w') as fh:
        fh.write('\n'.join(seeds))

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


def tactics_1st_gen(adj_list, outfile, num_seeds, n_players):
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
    print_to_file(final_selections, outfile)

def tactics_2nd_gen(adj_list, outfile, num_seeds, n_players):
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
    print_to_file(final_seeds, outfile)

def tactics_degree(adj_list, outfile, num_seeds, n_players):
    G = parse_graph(adj_list)
    degrees = G.degree()
    top_degree = [k[0] for k in sorted(degrees, key=lambda t: t[1], reverse=True)]

    TA_set = top_degree[:num_seeds]
    neighbors_of_top_dog = G[TA_set[0]]
    top_neighbors = [t for t in TA_set if t in neighbors_of_top_dog]
    seeds = TA_set[:num_seeds-1]

    TA_set = top_degree[:num_seeds]
    best = 0
    final_seeds = []
    for n in G[TA_set[0]]:
        simulation = sim.run(adj_list, {'us': seeds + [n], 'them': TA_set})
        if simulation['us'] > best:
            print('{} -> {}'.format(best, simulation['us']))
            best = simulation['us']
            final_seeds = seeds + [n]


    print(sim.run(adj_list, {'us': final_seeds, 'them': TA_set}))
    print_to_file(final_seeds * 50, sys.argv[2])

def tactics_fewer(adj_list, outfile, num_seeds, n_players):
    G = parse_graph(adj_list)
    degrees = G.degree()
    top_degree = [k[0] for k in sorted(degrees, key=lambda t: t[1], reverse=True)]

    TA_set = top_degree[:num_seeds - 2]

    neighbors_of_top_dog = G[TA_set[0]]
    # nbrs = [k[0] for k in sorted(G.degree(G[TA_set[0]]), key=lambda t: t[1], reverse=True) if k[0] not in seeds and k[0] not in TA_set]

    # seeds.append(nbrs[0])

    seeds = set(TA_set)
    nbrs = [k[0] for k in sorted(G.degree(G[TA_set[0]]), key=lambda t: t[1], reverse=True)]
    i = 0
    while len(seeds) < num_seeds:
        seeds.add(nbrs[i])
        i += 1

    seeds = list(seeds)
    print(sim.run(adj_list, {'us': seeds, 'them': TA_set}))
    print_to_file(seeds * 50, outfile)




if __name__ == '__main__':
    """
    Usage:

    python3 tactics.py name_of_strategy input_file number_of_seeds number_of_players

    """
    funcs = {
        '1st_gen': tactics_1st_gen,
        '2nd_gen': tactics_2nd_gen,
        'fewer': tactics_fewer,
        'degree': tactics_degree
    }

    try:
        with open(sys.argv[2], 'r') as fh:
            adj_list = json.loads(fh.read())
        funcs[sys.argv[1]](adj_list,
                           'results/{}'.format(sys.argv[2].split('/')[1]),
                           int(sys.argv[3]),
                           int(sys.argv[4]))
    except IndexError as e:
        print('FEED ME A GRAPH')
        print('     (ಠ‿ಠ)     ')
