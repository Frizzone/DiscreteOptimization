
import localsearch.twoOptHeurisct as twoOptHeurisct
import functions
import time

#2-opt Local Search Heuristic 
#using Iterated Local Search: starting from different starting configuration
def twoOptIterateLS(points, nodeCount, timeout):
    bestl = None
    bestSolution = None
    timeout = time.time() + timeout
    while True:
        solution  = twoOptHeurisct.twoOptHeurisct(points, nodeCount)
        l = functions.tourLength(solution, points, nodeCount)
        if(bestl == None or l < bestl):
            bestl = l
            bestSolution = solution
        #print(str(bestl))
        if time.time() > timeout: break
    return bestSolution
