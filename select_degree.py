import heapq

def select_degree(graph, num_seeds):
	"""
	Takes in an undirected graph represented by (key, value) pairs
	of (node, list of neighbors of node) and outputs the top <num_seeds> seed nodes
	ranked by degree
	"""

	nodes = []
	degrees = {}

	for node, neighbors in graph.items():
		degree = len(neighbors)
		degrees[node] = degree

	best_degrees = []

	for node in graph.keys():
		heapq.heappush(best_degrees, (-degrees[node], node))

	for k in range(0, num_seeds):
		nodes.append(heapq.heappop(best_degrees)[1])

	return nodes