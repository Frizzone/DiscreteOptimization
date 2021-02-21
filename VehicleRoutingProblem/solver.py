#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import networkx as nx
import matplotlib.pyplot as plt
import functions
import MixIntegerProgram.vpr_mip_gurobi as vpr_mip_gurobi
import GeneticAlgorithm.vpr_ga as vpr_ga
import LocalSearch.twoOptHeurisct as twoOptHeurisct

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(functions.Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0]

    if(customer_count < 25):
        vehicle_tours = vpr_mip_gurobi.vpr_mip_gurobi(customers, vehicle_count, vehicle_capacity)
    else:
        
        vehicle_tours = vpr_ga.vpr_geneticAlgorithm(customers=customers, vehicle_count=vehicle_count, vehicle_capacity=vehicle_capacity, popSize=100, eliteSize=10, mutationRate=0.1, generations=200)
        
        #local search for individual routes
        for v in range(vehicle_count):
            vehicle_tours[v] = twoOptHeurisct.twoOptHeurisct(vehicle_tours[v])
    
    #functions.DrawNetwork(vehicle_tours, customers, vehicle_count)

    # checks that the number of customers served is correct
    #assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = functions.tourLen(vehicle_tours, vehicle_count, depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        #outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'
        outputData += ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + '\n'

    
    return outputData

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

