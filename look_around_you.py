def look_around_you(G, num_seeds, n_players):
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

