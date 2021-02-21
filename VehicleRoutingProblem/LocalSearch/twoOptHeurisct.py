
import functions

#2-opt Local Search Heuristic
def twoOptHeurisct(solution,  points, nodeCount):
    for i in range(nodeCount-1):
        for j in range(nodeCount-1):
            if(isNeighborhood2opt(i, j, points, solution) == True): 
                if(i<j): swap2opt(solution, i, j)
                elif(i>j): swap2opt(solution, j, i)
    return solution

#isNeighborhood2opt:
#considering 4 points A->B and D->E
#when  A->B + D->E > A->D + B->E then it is a legal move = local improvement
def isNeighborhood2opt(i, j, points, solution):
    #intersectNode = (i!=j and (i<=j-2 or i>=j+2) and intersect(points[solution[i]], points[solution[i+1]], points[solution[j]], points[solution[j+1]]))
    improve = isImprovement(i, j, points, solution)
    return improve

def isImprovement(i, j, points, solution):
    actual = functions.length(points[solution[i]], points[solution[i+1]]) +  functions.length(points[solution[j]], points[solution[j+1]])
    new = functions.length(points[solution[i]], points[solution[j]]) +  functions.length(points[solution[i+1]], points[solution[j+1]])
    return new < actual

# A->B->C->D->E (A->B ..... D->E)
# A->D->C->B->E (A->D-> reverse(......) ->B->E)
def swap2opt(solution, start, end):
    solution[start+1:end+1] = reversed(solution[start+1:end+1])