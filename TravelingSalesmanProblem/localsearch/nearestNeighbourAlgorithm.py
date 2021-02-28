import functions
from random import seed
from random import randint
seed(1)

def nearestNeighbourAlgorithm(points, nodeCount):
    solution = []
    finish = False
    selected = [0]*nodeCount

    first = firstNode(points, nodeCount)
    solution.append(first)
    selected[first] = 1

    while(not finish):
        minlength = 0
        j = 0
        nextNode = j
        if(len(solution) < nodeCount):
            for j in range(nodeCount):
                if(selected[j]==0): 
                    l = functions.length(points[solution[-1]], points[j])
                    if(minlength == 0 or minlength > l): 
                        minlength = l
                        nextNode = j
            solution.append(nextNode)
            selected[nextNode] = 1            
        else: finish = True
    return solution

def firstNode(points, nodeCount):
    init = randint(0, nodeCount-1)
    return init