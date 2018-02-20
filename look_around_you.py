import networkx as nx
import numpy as np
import sys
import json

def print_to_file(seeds, filename):
    print('Printing {} lines to file {}'.format(len(seeds), filename))
    with open(filename, 'w') as fh:
        fh.write('\n'.join(seeds))

def parse_graph(adj_list):
    G = nx.Graph()
    for key in adj_list.keys():
        G.add_edges_from([(key, val) for val in adj_list[key]])
    return G

def look_around_youG(adj_list, outfile, n_seeds, n_players):
    G = parse_graph(adj_list)
    degrees = G.degree()
    top_degree = [k[0] for k in sorted(degrees, key=lambda t: t[1], reverse=True)]

    TA_set = set(top_degree[:n_seeds])
    reach = dict()
    for TA_seed in TA_set:
        reach = update_reach(G, reach, TA_seed)

    taken = TA_set
    our_choices = list()
    for i in range(n_seeds):
        new_node = highest_value_node(G, reach)
        reach = update_reach(G, reach, new_node)
        our_choices.append(new_node)
    with open(outfile, 'w') as fh:
        fh.write('\n'.join(our_choices))

def look_around_you(adj_list, outfile, n_seeds, n_players):
    G = parse_graph(adj_list)
    degrees = G.degree()
    top_degree = [k[0] for k in sorted(degrees, key=lambda t: t[1], reverse=True)]

    TA_set = set(top_degree[:n_seeds])
    reach = dict()
    for TA_seed in TA_set:
        reach = update_reach(G, reach, TA_seed)

    taken = TA_set
    our_choices = list()
    for i in range(n_seeds):
        new_node = highest_value_node(G, reach)
        reach = update_reach(G, reach, new_node)
        our_choices.append(new_node)
    with open(outfile, 'w') as fh:
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
    new_reach = nx.shortest_path_length(G, source = newnode)
    for node in new_reach:
        reach[node] = min(reach.get(node, float('inf')), new_reach[node])
    return reach

def node_value(G, reach, node):
    new_reach = nx.shortest_path_length(G, source = node)
    result = 0
    for node in new_reach:
        if(reach.get(node, float("inf")) > new_reach[node]):
            result += 1
    return result

