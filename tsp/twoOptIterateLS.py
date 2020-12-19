
import twoOptHeurisct
import functions
import time

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
