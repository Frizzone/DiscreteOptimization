import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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
        cl = [np.random.rand(3,)]

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
