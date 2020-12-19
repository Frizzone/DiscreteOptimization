#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy

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