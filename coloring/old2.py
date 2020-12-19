#!/usr/bin/python
# -*- coding: utf-8 -*-

SOURCE = 0
DESTINATION = 1
FEASIBLE = 0
INFEASIBLE = 1

import copy

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
    solution = constraintProgramming(edges, node_count)

    #if(validadeSolution(edges, solution)): print ("A solução é válida")
    #else: print ("A solução não é válida")

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def constraintProgramming(edges, node_count):
    #domínio = 0
    #fora do domínio = 1
    domainSpace = [[0 for x in range(2)] for x in range(node_count)]

    #colors table
    nodesColor = [-1]*node_count

    #orderna nós
    nodes = getOrderedNodes(edges, node_count)



    #print (domainSpace)
    return nodesColor

def branch(edges, domainSpace, nodes, nodeIndex, node_count, color_count):

    #print (str(node) + "-> " + str(color))
    #print (colors)
    #print (domainSpace)


    if(nodeIndex+1<=node_count-1):
        minValueOld = -1
        
        for nextcolor in feasibleColors(domainSpace, nodes[nodeIndex+1].index):

            #prunning
            newDomainSpace =  copy.deepcopy(domainSpace)
            feasible = constraintPropagate(newDomainSpace, nodes[nodeIndex+1].index, nextcolor)
            
            if(feasible):
                nodes[index+1].color = nextcolor
                #branch nextColor
                result = branch(edges, newDomainSpace, nodeIndex+1, nodes, node_count, color_count)
        
        #return the best solution
        return result
    else: 
        #last node (leaf)
        return 0


def constraintPropagate(domainSpace, edges, node, color):

    return True

def feasibilityTest(domainSpace, edge):
    #CONSTRUIR OS CONJUNTOS OU TRABALHAR COM CONJUNTOS?
    domainSpace[edge[SOURCE]].symmetric_difference(edge[DESTINATION])

#domainSpace: matrix nodes X colors
    #domínio = 0
    #fora do domínio = 1
    #valor escolhio = 2
#node: node number - integer
#feasible Values: fasible colors numbers
def prunning(domainSpace, node, feasibleColor):
    for color in range(len(domainSpace[node])):
        if (color == feasibleColor): domainSpace[node][color] = FEASIBLE
        else: domainSpace[node][color] = INFEASIBLE

def feasibleColors(domainSpace, node):
    feasibleColors = []
    i=0
    for ds in domainSpace[node]: 
        if ds == FEASIBLE: feasibleColors.append(i)
        i=i+1
    return feasibleColors

def validadeSolution(edges, solution):
    for edge in edges:
        if(solution[edge[0]] == solution[edge[1]]): 
            print ("O nó " + str(edge[0]) + " não pode ter a mesma cor do nó " + str(edge[1]))
            return False
    return True

def getOrderedNodes(edges, node_count):
    nodes = []
    for node in range(node_count):
        count = sum(row.count(node) for row in edges)
        nodes.append(Node(node, count, -1))
    
    nodes.sort(reverse=True, key = lambda x: x.value)
    return nodes

def generateColorArray(nodes):
    nodesColor = [-1]*len(nodes)
    for node in nodes:
        nodesColor[node.index] = node.color
    return nodesColor

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

