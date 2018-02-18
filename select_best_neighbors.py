#import networkx as nx
import heapq

def select_best_neighbors(graph, num_seeds):
	"""
	Takes in an undirected graph represented by (key, value) pairs
	of (node, list of neighbors of node) and outputs the top <num_seeds> seed nodes
	ranked by (average degree of neighbors)*degree
	"""

	nodes = []
	degrees = {}

	for node, neighbors in graph.items():
		degree = len(neighbors)
		degrees[node] = degree

	best_ave_neighbors = []

	for node in graph.keys():
		ave_neighbor_degree = 0

		# get ave degrees of neighbors for this node
		for neighbor in graph[node]:
			ave_neighbor_degree += degrees[neighbor]

		heapq.heappush(best_ave_neighbors, (-ave_neighbor_degree, node))

	for k in range(0, num_seeds):
		nodes.append(heapq.heappop(best_ave_neighbors)[1])

	return nodes






















