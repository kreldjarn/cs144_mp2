import json
import numpy as np

def load_graph(filename):
	"""
	Takes in the name of a file containing a JSON encoding of 
	a dictionary that represents a graph
	"""

	with open(filename) as graph_file:
		graph = json.load(graph_file)

		# maybe convert to numpy structured array to make things faster ?

	return graph


