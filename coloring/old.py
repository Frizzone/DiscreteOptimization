#!/usr/bin/python
# -*- coding: utf-8 -*-
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
    #domínio = 0 # fora do domínio = 1
    domainSpace = [[0 for x in range(2)] for x in range(node_count)]


    #solution = constraintProgramming(edges, domainSpace, nodesColor, 0, 0, node_count)
    solution = constraintProgrammingGreedy(edges, node_count)
    #value, solution = constraintProgramming(edges, [0], prunning(domainSpace, edges, 0, 0), 0, 0, node_count)

    #nodes = getOrderedNodes(edges,node_count)
    #nodes[0].color = 0
    #value, solution = constraintProgrammingBTFast(edges, prunning(domainSpace, edges, nodes[0].index, 0), 0, nodes , node_count)


    #if(validadeSolution(edges, solution)): print ("A solução é válida")
    #else: print ("A solução não é válida")

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

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
    return nodesColor

def constraintProgrammingBTFast(edges, domainSpace, index, nodes, node_count):

    #print (str(node) + "-> " + str(color))
    #print (colors)
    #print (domainSpace)

    if(index+1<=node_count-1):
        minValueOld = -1
        
        for nextcolor in feasibleColors(domainSpace, nodes[index+1].index):

            #prunning
            newDomainSpace =  copy.deepcopy(domainSpace)
            prunning(newDomainSpace, edges, nodes[index+1].index, nextcolor)
            
            #branch nextColor
            nodes[index+1].color = nextcolor
            minValue, currentResult = constraintProgrammingBTFast(edges, newDomainSpace, index+1, nodes, node_count)
            
            #choose best solution
            if(minValueOld != -1): 
                if(minValue < minValueOld): 
                    result = currentResult
            else:
                result = currentResult

            minValueOld = minValue
        
        #return the best solution
        return max(result), result
    else: 
        #last node (leaf)
        nodesColors = generateColorArray(nodes)
        return max(nodesColors), nodesColors
        

def constraintProgrammingBT(edges, colors, domainSpace, node, color, node_count):

    #print (str(node) + "-> " + str(color))
    #print (colors)
    #print (domainSpace)

    if(node+1<=node_count-1):
        minValueOld = -1
        for nextcolor in feasibleColors(domainSpace, node+1):
            #prunning
            newDomainSpace =  copy.deepcopy(domainSpace)
            prunning(newDomainSpace, edges, node+1, nextcolor)
            
            #branch nextColor
            minValue, currentResult = constraintProgrammingBT(edges, colors + [nextcolor], newDomainSpace, node+1, nextcolor, node_count)

            #choose best solution
            if(minValueOld != -1): 
                if(minValue < minValueOld): 
                    result = currentResult
            else:
                result = currentResult

            minValueOld = minValue
        
        #return the best solution
        return max(result), result
    else: 
        #last node (leaf)
        return max(colors), colors

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

def firtFeasible(domainSpace, node):
    try:
        return domainSpace[node].index(0)
    except ValueError:
         domainSpace[node].append(0)
         return domainSpace[node].index(0)

def feasibleColors(domainSpace, node):
    feasibleColors = []
    i=0
    for ds in domainSpace[node]: 
        if ds == 0: feasibleColors.append(i)
        i=i+1

    #não existe nenhum
    if(len(feasibleColors)==0): 
        domainSpace[node].append(0)
        return [i]

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

