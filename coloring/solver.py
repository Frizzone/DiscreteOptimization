#!/usr/bin/python
# -*- coding: utf-8 -*-
from constraint import *
from ortools.sat.python import cp_model

class Node:
    def __init__(self, index, value, color):
        self.index = index
        self.value = value
        self.color = color

    def setColor(self, color):
        self.color = color



def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    
    nodesColor = [-1]*node_count

    solution = ORToolsSolver(edges, node_count)


    #if(validadeSolution(edges, solution)): print ("A solução é válida")
    #else: print ("A solução não é válida")

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def ORToolsSolver(edges, node_count):

    model = cp_model.CpModel()

    num_colors = node_count

    nodeColors = []
    for node in range(node_count):
        nodeColors.append(model.NewIntVar(0, num_colors, str(node)))

    max_color = model.NewIntVar(0, num_colors, 'max_color')

    #restrição de max_color = max(nodeColors)
    model.AddMaxEquality(max_color, nodeColors)
    
    #adicionar restrições de nós adjacentes
    # se aresta(n1,n2) então nodeColor(n1) != nodeColor(n2)
    for e in edges:
        model.Add(nodeColors[e[0]] != nodeColors[e[1]])
        #usar AllDifferent para melhorar tempo

    # symmetry breaking
    # model.Add(nodeColors[0] == 1);
    # model.Add(nodeColors[1] <= 2);
    #for i in range(num_colors):
    #    model.Add(nodeColors[i] <= i+1)

    #função objetivo =  minimizar(max_color)
    model.Minimize(max_color)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

        
    solution = []
    for node in range(node_count): solution.append(solver.Value(nodeColors[node]))

    return solution


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

