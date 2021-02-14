import math
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt
from random import seed
from random import random

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def plot(tours, customers, vehicle_count):
    G=nx.Graph()
    
    pos = {}
    clist = []
    for c in customers:
        pos["c"+str(c.index)] = (c.location.x,c.location.y)
        clist.append("c"+str(c.index))
    
    nx.draw_networkx_nodes(G,pos,node_size=1,nodelist=clist,node_color='b')

  
    edges = []
    for v in range(vehicle_count):
        for i in range(len(tours[v])):
            if(i==0): edges.append(("c"+str(0), "c"+str(tours[v][i].index)))
            else: edges.append("c"+str(tours[v][i-1].index)), "c"+str(tours[v][i].index)))
        nx.draw_networkx_edges(G, pos, edgelist=edges)
    
    plt.show()

def DrawNetwork(tours, customers, vehicle_count):
    G = nx.DiGraph()
    
    locations = {}
    for c in customers:
        locations[str(c.index)] = (c.location.x,c.location.y)
    
    x = 0    
    for vehicle_id in range(len(vehicle_count)):
        n = 0
        e = []
        node = []
        cl = (random.random(), random.random(), random.random())

        for customer in tours[vehicle_id]:
            G.add_node(customer.index, pos=(customer.x, customer.y))
            if n > 0:
                u = (tours[vehicle_id][n-1].index, tours[vehicle_id][n].index)
                e.append(u)
                node.append(customer.index)
                G.add_edge(tours[vehicle_id][n-1].index, tours[vehicle_id][n].index)
                nx.draw(G, nx.get_node_attributes(G, 'pos'), nodelist=node, edgelist=e, with_labels=True,
                        node_color=cl, width=2, edge_color=cl,
                        style='dashed', font_color='w', font_size=12, font_family='sans-serif')
            n += 1
        x += 1
    
    nx.draw_networkx_nodes(G, locations, nodelist=[0], node_color='k')
    plt.axis('on')
    plt.show()

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)