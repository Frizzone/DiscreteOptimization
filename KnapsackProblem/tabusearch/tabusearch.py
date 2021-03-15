import matplotlib.pyplot as plt
import tabusearch.localSearchFS as lsfs
import tabusearch.localSearchUS as lsus

__BITMAX = 100000

def tabuSearch(items, capacity, option):
    solution = createGreedySolution(items, capacity)
    print (str(solution["value"]) + " " + str(solution["weight"]))
    
    it = 0
    bestIt = 0
    tabuList = list()
    bestValue = solution["value"]
    bestSolution = solution.copy()
    progress = []
    
    while (it - bestIt < __BITMAX):
        it += 1
        if(option=="4"): lsfs.localSearchNextMoveJustFeasible(solution, bestValue, capacity, items, tabuList)
        elif (option=="5"): lsus.localSearchNextMoveAllowUnfeasible(solution, bestValue, capacity, items, tabuList)
        
        progress.append(solution["value"])
        
        if(solution["feasible"]==True and bestValue < solution["value"]):
           bestValue = solution["value"]
           bestSolution = solution.copy()
           bestIt += 1
           print (str(bestSolution["value"]) + " " + str(bestSolution["weight"]))
        
    
    if(option=="4"):  print(str(lsfs.tabucount) + " - " + str((lsfs.tabucount)/(lsfs.tabucount+lsfs.tabuallow)))
    elif (option=="5"): print(str(lsus.tabucount) + " - " + str((lsus.tabucount)/(lsus.tabucount+lsus.tabuallow)))   
    
    plt.plot(progress)
    plt.ylabel('Object function')
    plt.xlabel('Iteration')
    plt.show() 
    
    return bestSolution

def createGreedySolution(items, capacity):
    solution = {"taken": [0]*len(items), "weight": 0, "value": 0, "feasible":True}
    items.sort(key = lambda x: (x.weight/x.value))

    for item in items:
        if solution["weight"] + item.weight <= capacity:
            solution["taken"][item.index] = 1
            solution["value"] += item.value
            solution["weight"] += item.weight
    return solution