import random
tabucount = 1
tabuallow = 1
_TSSIZEFACTOR = 2

def localSearchNextMoveJustFeasible(solution, bestValue, capacity, items, tabuList):
    
    tabuSize = _TSSIZEFACTOR * len(items)
    bestMove = {"weight": solution["weight"], "value": solution["value"], "index": -1}
    worstMove = {"weight": solution["weight"], "value": solution["value"], "index": -1}
    worseList = list()
    
    #evaluate the neighborhood
    for item in items:
        
        if(solution["taken"][item.index] == 0): operation = 1 #add
        elif(solution["taken"][item.index] == 1): operation = -1 #remove
        
        weight = solution["weight"] + item.weight * operation
        value = solution["value"] + item.value * operation
        if(operation == -1): operation=0
        move = {"weight": weight, "value": value,  "index": item.index, "rate":item.rate, "operation":operation}
        
        if(solution["taken"][item.index] == 0 
           and isFeasibleSolution(capacity, solution["weight"] + item.weight) 
           and isBestMove(bestMove["value"], solution["value"] + item.value)
           and isNotTabu(tabuList, bestValue, move)):
            bestMove["weight"] = move["weight"]
            bestMove["value"] = move["value"]
            bestMove["index"] = move["index"]
            bestMove["rate"] = move["rate"]
            bestMove["operation"] = move["operation"]

        
        elif(solution["taken"][item.index] == 1 
             and isWorseMove(worstMove["value"], solution["value"] - item.value)
             #and isNotTabu(tabuList, 0, item.index, solution["value"] - item.value)
             ):
            worstMove["weight"] = move["weight"]
            worstMove["value"] = move["value"]
            worstMove["index"] = move["index"]
            worstMove["rate"] = move["rate"]
            worstMove["operation"] = move["operation"]

        
        elif(solution["taken"][item.index] == 1 ): 
            worseList.append({"weight": solution["weight"] - item.weight, "value": solution["value"] - item.value, "index": item.index, "rate":item.rate})
    
    #select the bestmove
    if(bestMove["value"] > solution["value"]): 
        i = bestMove["index"]
        solution["taken"][i] = 1
        solution["value"] = bestMove["value"]
        solution["weight"] = bestMove["weight"]
        solution["rate"] = bestMove["rate"]
        updateTabuList(tabuList, tabuSize, bestMove)
    
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
    
def updateTabuList(tabuList, tabuSize, move):
    tabuList.append(move)
    while(len(tabuList) > tabuSize): tabuList.pop(0)
    
def isNotTabu(tabuList, bestValue, move):
    global tabuallow
    global tabucount
    
    #aspiration criteria: new local optimum
    if(move["value"] > bestValue):
        tabuallow = tabuallow+1
        return True
    
    #and then, allow only itens the is not tabu
    for tabuItem in tabuList:
        if(tabuItem["index"] == move["index"] and tabuItem["value"] == move["value"] and tabuItem["operation"]==move["operation"]):
            tabucount = tabucount+1
            return False
    tabuallow = tabuallow+1
    return True