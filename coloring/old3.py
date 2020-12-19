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

    greedySolution = constraintProgrammingGreedy(edges,node_count)
    solution = ORToolsSolver(edges, node_count, greedySolution)


    #if(validadeSolution(edges, solution)): print ("A solução é válida")
    #else: print ("A solução não é válida")

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def pythonConstraintSolver(edges, node_count, number_colors):
    #print (number_colors)
    lastSolution = None
    while (True):
        problem = Problem(MinConflictsSolver())
        for node in range(node_count):
            problem.addVariable(node, range(number_colors))
        
        for e in edges:
            problem.addConstraint(lambda a,b: a!=b, (e[0],e[1]))

        
        newsolution = problem.getSolution()

        if(newsolution == None): break

        
        number_colors=number_colors-1
        lastSolution = newsolution

    solution = []
    for key, value in lastSolution.items(): solution.append(value)

    return solution

def ORToolsSolver(edges, node_count, number_colors):
    

    lastSolution = None
    while (True):
        #print (number_colors)
        model = cp_model.CpModel()

        var = []
        for node in range(node_count):
            var.append(model.NewIntVar(0, number_colors, str(node)))
        
        for e in edges:
            model.Add(var[e[0]] != var[e[1]])
            #usar AllDifferent para melhorar tempo

        newsolution = cp_model.CpSolver()
        newsolution.parameters.max_time_in_seconds = 600.0
        status = newsolution.Solve(model)

        if(status == cp_model.INFEASIBLE or status == cp_model.UNKNOWN): break

        number_colors=number_colors-1
        lastSolution = newsolution
        
    solution = []
    for node in range(node_count): solution.append(lastSolution.Value(var[node]))

    return solution

def constraintProgrammingGreedy(edges, node_count):
    #domínio = 0
    #fora do domínio = 1
    domainSpace = [[0 for x in range(2)] for x in range(node_count)]

    #colors table
    nodesColor = [-1]*node_count

    #orderna nós
    nodes = getOrderedNodes(edges, node_count)

    #percorre nós
    for node in nodes:
        #acha primeira cor viável, dado o espaço do domínio permitido
        color = firtFeasible(domainSpace, node.index)

        #defini cor
        nodesColor[node.index] = color

        #capina o espaço de busca, baseado na nova escolha - Constraint propagation
        prunning(domainSpace, edges, node.index, color)

    #print (domainSpace)
    return max(nodesColor)+1

def firtFeasible(domainSpace, node):
    try:
        return domainSpace[node].index(0)
    except ValueError:
         domainSpace[node].append(0)
         return domainSpace[node].index(0)

def getOrderedNodes(edges, node_count):
    nodes = []
    for node in range(node_count):
        count = sum(row.count(node) for row in edges)
        nodes.append(Node(node, count, -1))
    
    nodes.sort(reverse=True, key = lambda x: x.value)
    return nodes

def prunning(domainSpace, edges, node, color):
    for e in edges:
        if(e[0] == node): 
            addColorsToDomain(domainSpace, e[1], color)
            domainSpace[e[1]][color] = 1
        if(e[1] == node): 
            addColorsToDomain(domainSpace, e[0], color)
            domainSpace[e[0]][color] = 1

    return domainSpace

def addColorsToDomain(domainSpace, node, color):
    while(len(domainSpace[node]) <= color): domainSpace[node].append(0)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

