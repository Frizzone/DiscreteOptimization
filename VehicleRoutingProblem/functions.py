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
                        node_color=cl, width=1, edge_color=cl, node_size=35,
                        style='dashed', font_color='w', font_size=6, font_family='sans-serif')
            n += 1
        x += 1
    
    nx.draw_networkx_nodes(G, locations, nodelist=[0], node_color='k', node_size=50)
    plt.axis('on')
    plt.show()

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

# calculate the cost of the solution; for each vehicle the length of the route
def tourLen(vehicle_tours, vehicle_count, depot):
    obj = 0
    for v in range(0, vehicle_count):
        if len(vehicle_tours[v]) > 0: obj += routeLen(vehicle_tours[v], depot)
    return obj

# calculate the cost of the solution; for each vehicle the length of the route
def routeLen(vehicle_route, depot):
    obj = 0
    obj += length(depot,vehicle_route[0])
    for i in range(0, len(vehicle_route)-1):
        obj += length(vehicle_route[i],vehicle_route[i+1])
    obj += length(vehicle_route[-1],depot)
    return obj

def bestTour(vehicle_tours, depot):
    minTour = vehicle_tours[0]
    minlen = routeLen(vehicle_tours[0], depot)
    for i in range (1, len(vehicle_tours)):
        actuallen = routeLen(vehicle_tours[i], depot)
        if(actuallen<minlen): 
            minlen = actuallen
            minTour = vehicle_tours[i]
    return (minTour, minlen)
        

def nearestNode(customers, customer, selected):
    nearestNode = 0
    minlength = 0
    for j in range(len(customers)):
        if(selected[customers[j].index] == 0 and customers[j].index != 0):
            l = length(customer, customers[j])
            if(minlength == 0 or minlength > l): 
                minlength = l
                nearestNode = j
    if nearestNode!=0: return customers[nearestNode]
    else: return None
    