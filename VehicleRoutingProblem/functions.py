import math
from collections import namedtuple

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

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
    