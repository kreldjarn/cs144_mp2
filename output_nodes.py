import json

from load_graph import load_graph
from select_best_neighbors import select_best_neighbors
from select_degree import select_degree

# select the graph and the allowed number of seeds
graph = load_graph('testgraph1.json')
num_seeds = 10

# save nodes as text file

# print nodes 50 times for different selection strategies

filename = 'nodes_best_neighbors.txt'
with open(filename, 'w') as nodes_file:

	# get seed nodes list for 50 games
	for k in range(0,50):
		nodes = select_best_neighbors(graph, num_seeds)

		# write nodes to file
		for node in nodes:
			nodes_file.write(node + '\n')

filename = 'nodes_degree.txt'
with open(filename, 'w') as nodes_file:

	# get seed nodes list for 50 games
	for k in range(0,50):
		nodes = select_degree(graph, num_seeds)

		# write nodes to file
		for node in nodes:
			nodes_file.write(node + '\n')








