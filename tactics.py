#!/usr/bin/env python3

# Standard library dependencies
# =============================
import sys
import json

# Third-party dependencies
# ========================
import networkx as nx

def parse_graph(adj_list):
    G = nx.Graph()
    for key in graph.keys():
        G.add_edges_from([(key, val) for val in adj_list[key]])
    return G

def tactics(adj_list):
    G = parse_graph(adj_list)
    print(G)


if __name__ == '__main__':
    try:
        with open(sys.argv[1], 'r') as fh:
            adj_list = json.loads(fh.read())
        tactics(adj_list)
    except IndexError as e:
        print('FEED ME A GRAPH')
        print('     (ಠ‿ಠ)     ')
