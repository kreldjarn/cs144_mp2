# Standard library dependencies
# =============================
import sys
import json
import random
import math
import sim
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import collections

# Our functions
# =============

def parse_graph(adj_list):
    G = nx.Graph()
    for key in adj_list.keys():
        G.add_edges_from([(key, val) for val in adj_list[key]])
    return G
    

def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield o
    
def print_to_file(seeds, filename):
    print('Printing {} lines to file {}'.format(len(seeds), filename))
    with open(filename, 'w') as fh:
        fh.write('\n'.join(seeds))
    
#%% open a graph

with open('TA_more_test/2.10.32.json') as fh:
    adj_list = json.load(fh)
G=parse_graph(adj_list)     


# open TA nodes
with open('test_data/2.10.32-LBMK.json') as fh:
    adj_list = json.load(fh)
    theirs=adj_list["TA_more"]
TA_picks=list(traverse(theirs))

#%% plot a graph
d = nx.degree(G)

pos=nx.spring_layout(G) # positions for all nodes
nx.draw_networkx_nodes(G,pos,node_size=10)

plt.figure(3,figsize=(5,5)) 
nx.draw(G,pos,node_size=5,width=.01)
plt.savefig('./graphvis/2.10.30.pdf', format='pdf', dpi=1000, bbox_inches='tight')
plt.show()
                    
 #%% plot degree distribution histograms

degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence

plt.figure()
plt.hist(degree_sequence,50,color='b')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.savefig('./graphvis/2.10.33_hist.pdf', format='pdf', dpi=1000, bbox_inches='tight')

#%% get number of times the TA picked each node, color graph nodes by this       
pick_count={}
for node in TA_picks:
    pick_count[node]=TA_picks.count(node)
    
    
# node colors
#default should be grey, otherwise color from yellow to red based on number of times picked 
colors=[]
sizes=[]
for node in list(G.nodes):
    if node in TA_picks:
        colors.append('r')
        sizes.append(40)
    else:
        colors.append(0.6)
        sizes.append(5)
        
plt.figure()
pos=nx.spring_layout(G) # positions for all nodes
nx.draw_networkx_nodes(G,pos,node_size=sizes,width=.06,cmap=plt.get_cmap('jet'),node_color=colors)
plt.savefig('graphvis/2.10.32_TApicks.pdf', format='pdf', dpi=1000, bbox_inches='tight')
    
#%% color graph plot nodes by their degree
deg_list=[]
for n, d in G.degree():
    deg_list.append(d)
plt.figure(3,figsize=(12,12)) 
#pos=nx.spring_layout(G) # positions for all nodes
nx.draw_networkx_nodes(G,pos,node_size=20,width=.06,cmap=plt.get_cmap('jet'),node_color=deg_list)
#plt.savefig('graphvis/2.10.30_degree.pdf', format='pdf', dpi=1000, bbox_inches='tight')
plt.show()

#%% replace values in 'theirs' with node degree

theirdegrees=[]
for submission in theirs:
    degrees=[]
    for i in range(4):
        degrees.append(d[submission[i]])
    theirdegrees.append(degrees)    
    
TA_degrees=list(traverse(theirdegrees))


degree_sequence = sorted(TA_degrees, reverse=True)  # degree sequence
# print "Degree sequence", degree_sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')

plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
#ax.set_xticks([d + 0.4 for d in deg])
ax.set_xticklabels(deg)


#%% TA_more's pick fractions of degree
TA_ints=np.array(theirs,dtype=int)
d = nx.degree(G)
theirdegrees=[]
for submission in theirs:
    degrees=[]
    for i in range(12):
        degrees.append(d[submission[i]])
    theirdegrees.append(degrees)    


ranked_degrees=[]
for node in G.nodes:
    ranked_degrees.append(d[node])
ranked_degrees=sorted(ranked_degrees,reverse=True)

sum_top12=np.sum(ranked_degrees[:12])    

 
frac_degrees=np.sum(np.array(theirdegrees,dtype=int),1)/sum_top12
plt.figure()
plt.plot(frac_degrees) 
plt.xlabel('TA choice')
plt.ylabel('Fraction of pick\'s top degree')
plt.savefig('graphvis/2.10.32_frac.pdf', format='pdf', dpi=1000, bbox_inches='tight')
    

#%% strategy 1

with open('./test_data/8.40.1.json') as fh:
    adj_list = json.load(fh)
G=parse_graph(adj_list) 

degrees = G.degree()
top_degree = [k[0] for k in sorted(degrees, key=lambda t: t[1], reverse=True)]



final_seeds=[]
for iter in range(50):
    seeds=[]
    p=float(np.random.rand(1))
    if p>= 0.2:
       # pick top 10 
       top10=top_degree[:40] 
       final_seeds.append(top10)
    else:
        # pick top num_seeds/2 and and random neighbor of each
        top5=top_degree[:20]
        top5nbrs=[]
        for node in top5:
            neighbors=adj_list[node]
            nbr=random.choice(neighbors)
            top5nbrs.append(nbr)
        top10_5=top5+top5nbrs 
        final_seeds.append(top10_5) 

# open TA nodes
with open('test_data/2.10.31-LBMK.json') as fh:
    TA_adj_list = json.load(fh)
    TA_set=TA_adj_list["TA_more"]
   
print(sim.run(adj_list, {'us': ['1','2','3','4','5'], 'them': ['2','4','6','8','10']}))   
#print_to_file(list(traverse(final_seeds)), 'results/8.40.1.txt')


#%% strategy 2
with open('./test_data/8.30.1.json') as fh:
    adj_list = json.load(fh)
G=parse_graph(adj_list) 

degrees = G.degree()
top_degree = [k[0] for k in sorted(degrees, key=lambda t: t[1], reverse=True)]



final_seeds=[]
for iter in range(50):
    seeds=[]
    p=float(np.random.rand(1))
    if p>= 0.7:
       # pick top 10 
       top10=top_degree[:30] 
       final_seeds.append(top10)
    else:
        # pick top num_seeds/2 and and random neighbor of each
        top5=top_degree[:15]
        top5nbrs=[]
        for node in top5:
            neighbors=adj_list[node]
            maxnbr=neighbors[0]
            for nbr in neighbors:
                if degrees[nbr]>=degrees[maxnbr]:
                    maxnbr=nbr
            top5nbrs.append(maxnbr)
        top10_5=top5+top5nbrs 
        final_seeds.append(top10_5) 

# open TA nodes
with open('test_data/2.10.31-LBMK.json') as fh:
    TA_adj_list = json.load(fh)
    TA_set=TA_adj_list["TA_more"]
   
#print(sim.run(adj_list, {'us': ['1','2','3','4','5'], 'them': ['2','4','6','8','10']}))   
print_to_file(list(traverse(final_seeds)), 'results/8.30.1.txt')
  
# 2.10.32, p=0.5 s1
# 8.10.3, p=0.5 s1
# 8.20.4, p=0.5, s2
# 8.30.1, p=0.7, s2
# 8.40.1, p=0.2, s1
