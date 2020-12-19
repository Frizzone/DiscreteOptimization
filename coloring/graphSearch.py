#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy

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

    #call graph search
    solution = exhaustive_search(0, edges, [0], node_count, 0)
    while -1 in solution: 
        temp = exhaustive_search(solution.index(-1), edges, [solution.index(-1)], node_count, 0)
        mergeSolution(solution, temp, node_count)

    #if(validadeSolution(edges, solution)): print ("A solução é válida")
    #else: print ("A solução não é válida")

    # prepare the solution in the specified output format
    #output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    #output_data += ' '.join(map(str, solution))

    #return output_data

def test(nodesColor):
    nodesColor[0] = 10
    print(nodesColor)

def exhaustive_search(node, edges, path, node_count, maxValue):
    nextNodes = listNextNodes(node, edges)

    colors = defineColorPath(edges, path, node_count)
    
    #print(path)

    for n in nextNodes:
        if(not isLoop(n, path)):
            temp = exhaustive_search(n, edges, path + [n], node_count, maxValue)
            mergeSolution(colors, temp, node_count)

    print (path)
    print (colors)
    return colors

def greedy(node, edges, path, node_count, maxValue):
    nextNodes = listNextNodes(node, edges)

    colors = defineColorPath(edges, path, node_count)
    
    for n in nextNodes:
        if(not isLoop(n, path) and colors[n] == -1):
            temp = greedy(n, edges, path + [n], node_count, maxValue)
            mergeSolution(colors, temp, node_count)
    return colors

def listNextNodes(node, edges):
    nodes = []
    for e in edges:
        if(e[0] == node): nodes.append(e[1])
        if(e[1] == node): nodes.append(e[0])
    return nodes

def isLoop(node, path):
    for n in path:
        if(n == node): return True
    return False

def defineColorPath(edges, path, node_count):
    colors = [-1]*node_count
    for node in path:
        nextNodes = listNextNodes(node, edges)
        colors[node] = defineColorNode(nextNodes, colors, node)
    return colors

def defineColorNode(nextNodes, colors, node):
    numbers = []
    for nextNode in nextNodes: numbers.append(colors[nextNode])

    #ordena
    numbers.sort()

    #remove -1
    while -1 in numbers: numbers.remove(-1)

    #remove duplicadas
    numbers = list(dict.fromkeys(numbers))

    i=0
    for n in numbers: 
        if(n==i): i=i+1
        else: return i
    return i

import sys

def mergeSolution(colors, temp, node_count):
    for i in range(node_count): 
        if(colors[i] == -1 and temp[i] != -1): colors[i] = temp[i]

def validadeSolution(edges, solution):
    for edge in edges:
        if(solution[edge[0]] == solution[edge[1]]): 
            print ("O nó " + str(edge[0]) + " não pode ter a mesma cor do nó " + str(edge[1]))
            return False
    return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

