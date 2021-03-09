import random, matplotlib.pyplot as plt
__BTMAX = 100000
_TSSIZE = 0.9

from collections import namedtuple
ItemTabu = namedtuple("ItemTabu", ['index', 'operation', 'value'])

def tabuSearch(items, capacity):
    solution = createGreedySolution(items, capacity)
    print (str(solution["value"]) + " " + str(solution["weight"]))
    
    it = 0
    bestIt = 0
    tabuList = list()
    tabuSize = 1000
    bestValue = solution["value"]
    bestSolution = solution.copy()
    progress = []
    
    while (it - bestIt < __BTMAX):
        it += 1
        localSearchNextMove(solution, bestValue, capacity, items, tabuList, tabuSize)
        progress.append(solution["value"])
        #print (str(solution["value"]) + " " + str(solution["weight"]))
        if(bestValue < solution["value"]):
           bestValue = solution["value"]
           bestSolution = solution.copy()
           bestIt += 1
           print (str(bestSolution["value"]) + " " + str(bestSolution["weight"]))
    
    plt.plot(progress)
    plt.ylabel('Object function')
    plt.xlabel('Iteration')
    plt.show() 
    
    return bestSolution

def createGreedySolution(items, capacity):
    solution = {"taken": [0]*len(items), "weight": 0, "value": 0}
    items.sort(key = lambda x: (x.weight/x.value))

    for item in items:
        if solution["weight"] + item.weight <= capacity:
            solution["taken"][item.index] = 1
            solution["value"] += item.value
            solution["weight"] += item.weight
    return solution                
                
def localSearchNextMove(solution, bestValue, capacity, items, tabuList, tabuSize):
    bestMove = {"weight": solution["weight"], "value": solution["value"], "index": -1, "rate":0}
    worstMove = {"weight": solution["weight"], "value": solution["value"], "index": -1, "rate":99999}
    worseList = list()

    #evaluate the neighborhood
    for item in items:
        if(solution["taken"][item.index] == 0 
           and isFeasibleSolution(capacity, solution["weight"] + item.weight) 
           and isBestMove(bestMove["value"], solution["value"] + item.value)
           and isNotTabu(tabuList, bestValue, 1, item.index, solution["value"] + item.value)):
            bestMove["weight"] = solution["weight"] + item.weight
            bestMove["value"] = solution["value"] + item.value
            bestMove["index"] = item.index
            bestMove["rate"] = item.rate
            #break; #first improvement
        
        elif(solution["taken"][item.index] == 1 
             and isWorseMove(worstMove["value"], solution["value"] - item.value)
             #and isNotTabu(tabuList, 0, item.index, solution["value"] - item.value)
             ):
            worstMove["weight"] = solution["weight"] - item.weight
            worstMove["value"] = solution["value"] - item.value
            worstMove["index"] = item.index
            worstMove["rate"] = item.rate
            #break; #first improvement
        
        
        elif(solution["taken"][item.index] == 1 ): 
            worseList.append({"weight": solution["weight"] - item.weight, "value": solution["value"] - item.value, "index": item.index, "rate":item.rate})
    
    #select the bestmove
    if(bestMove["value"] > solution["value"]): 
        i = bestMove["index"]
        solution["taken"][i] = 1
        solution["value"] = bestMove["value"]
        solution["weight"] = bestMove["weight"]
        updateTabuList(tabuList, i, 1, bestMove["value"], tabuSize)
    
    #diversification - local-optima avoidance: select the worst value or the rate
    else:
        if(len(worseList) == 0 or random.random()>0.5):
            i = worstMove["index"]
            solution["taken"][i] = 0
            solution["value"] = worstMove["value"]
            solution["weight"] = worstMove["weight"]
        else:
            worseMove = worseList.pop(0)
            i = worseMove["index"] 
            solution["taken"][i] = 0
            solution["value"] = worseMove["value"]
            solution["weight"] = worseMove["weight"]
            
def isBestMove(bestValue, newvalue):
    if(newvalue > bestValue): return True
    else: return False

def isWorseMove(worsevalue, newvalue):
    if(newvalue <= worsevalue): return True
    else: return False        

def isFeasibleSolution(capacity, newweight):
    if(capacity >= newweight): return True
    else: return False
    
def updateTabuList(tabuList, index, operation, value, tabuSize):
    tabuList.append(ItemTabu(index, operation, value))
    while(len(tabuList) > tabuSize): tabuList.pop(0)
    
def isNotTabu(tabuList, bestValue, operation, index, newvalue):
    if(newvalue > bestValue): return True
    for tabuItem in tabuList:
        if(tabuItem.index == index and tabuItem.value == newvalue and tabuItem.operation==operation):
            return False
    return True