import math
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def DrawNetwork(tours, customers, vehicle_count):
    G = nx.DiGraph()
    
    locations = {}
    locations[0] = (0,0)
    for c in customers:
        locations[c.index] = (c.x,c.y)
    
    x = 0    
    for vehicle_id in range(vehicle_count):
        n = 0
        e = []
        node = []
        cl = np.random.rand(3,)

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

# calculate the cost of the solution; for each vehicle the length of the route
def tourLen(vehicle_tours, vehicle_count, depot):
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot,vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(vehicle_tour[i],vehicle_tour[i+1])
            obj += length(vehicle_tour[-1],depot)
    return obj