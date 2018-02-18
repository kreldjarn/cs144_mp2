import sim
from load_graph import load_graph

from select_best_neighbors import select_best_neighbors
from select_degree import select_degree

graph_name = 'testgraph2.json'
graph = load_graph(graph_name)
num_seeds = 10

strategies = {}
strategies['player1'] = select_best_neighbors(graph, num_seeds)
strategies['player2'] = select_degree(graph, num_seeds)

results = sim.run(graph, strategies)

for player, winnings in sorted(results.items()):
	print(str(player) + " got " + str(winnings) + " nodes")