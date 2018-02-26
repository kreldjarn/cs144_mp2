#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 14:24:20 2018

@author: Lucien
"""

import sys
import json

# Third-party dependencies
# ========================
import networkx as nx
import numpy as np

def selector(G,num_seeds,bestboys):

    #input variables: bestboys, G, num_seeds
    num_seeds-=1
    focus=bestboys[0]
    i=1
    while num_seeds > len(G[focus]):
        focus=bestboys[i]
        i+=1
        
    seeds=[focus]
    indices=np.ndarray.tolist(np.random.randint(0, len(G[focus]),num_seeds)) #pick at random
    
    for index in indices:
        seeds.append(list(nx.all_neighbors(G, focus))[index])
        
    return seeds

    
    
    