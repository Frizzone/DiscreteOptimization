import random
tabucount = 1
tabuallow = 1
_TSSIZEFACTOR = 0.8

def localSearchNextMoveAllowUnfeasible(solution, bestValue, capacity, items, tabuList):
    moves = []
    tabuSize = _TSSIZEFACTOR * len(items)
    
    #create a neighborhood list
    for item in items:      
        if(solution["taken"][item.index] == 0): operation = 1 #add
        elif(solution["taken"][item.index] == 1): operation = -1 #remove
        
        weight = solution["weight"] + item.weight * operation
        value = solution["value"] + item.value * operation
        evaluationValue = solution["value"] + item.value * operation
        
        #apply penalty for unfeasible
        if(not isFeasibleSolution(capacity, weight)):
            evaluationValue = value - 2 * bestValue * ((weight-capacity)/capacity)
        
        if(operation == -1): operation=0
        solutioncopy = solution["taken"].copy()
        solutioncopy[item.index] = operation
        moves.append({"weight": weight, "value": value, "evaluationValue": evaluationValue, "index": item.index, "rate":item.rate, "operation":operation, "solution":solutioncopy})

    #evaluate the neighborhood
    bestMove = {"weight": -1, "value": -1, "evaluationValue": -1, "index": -1, "rate":-1, "operation":-1, "solution":-1}
    removeMoves = list()
    for move in moves:
        if(bestMove == None or (move["evaluationValue"] > bestMove["evaluationValue"]
                                and isNotTabu(tabuList, bestValue, move))): 
            bestMove = move
        if(move["operation"] == 0): 
            removeMoves.append(move)

    ##diversification - local-optima avoidance: randonly select item (10% of chance)
    if(random.random() < 0.1):
        x = random.randint(0, len(moves)-1)
        selectedMove = moves.pop(x)
        i = selectedMove["index"] 
        solution["taken"][i] = selectedMove["operation"]
        solution["value"] = selectedMove["value"]
        solution["weight"] = selectedMove["weight"]
        solution["feasible"] = (selectedMove["weight"] <= capacity)
        updateTabuList(tabuList, tabuSize, bestMove)
    
    #select the bestmove 90% chance
    elif(bestMove["value"] != -1): 
        i = bestMove["index"]
        solution["taken"][i] = bestMove["operation"]
        solution["value"] = bestMove["value"]
        solution["weight"] = bestMove["weight"]
        solution["feasible"] = (bestMove["weight"] <= capacity)
        updateTabuList(tabuList, tabuSize, bestMove)
    
    #diversification: tabu list is full, then remove random item
    else:
        x = random.randint(0, len(removeMoves)-1)
        selectedMove = removeMoves.pop(x)
        i = selectedMove["index"] 
        solution["taken"][i] = 0
        solution["value"] = selectedMove["value"]
        solution["weight"] = selectedMove["weight"]
        solution["feasible"] = (selectedMove["weight"] <= capacity)

def isFeasibleSolution(capacity, newweight):
    if(capacity >= newweight): return True
    else: return False

def isNotTabu(tabuList, bestValue, move):
    global tabuallow
    global tabucount
    
    #and then, allow only itens the is not tabu
    for tabuItem in tabuList:
        if(tabuItem["index"] == move["index"] 
           #and tabuItem["value"] == move["value"] 
           #and tabuItem["operation"]==move["operation"]
           ):
            tabucount = tabucount+1
            return False
    tabuallow = tabuallow+1
    return True

def updateTabuList(tabuList, tabuSize, move):
    tabuList.append(move)
    while(len(tabuList) > tabuSize): tabuList.pop(0)