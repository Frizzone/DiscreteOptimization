
import functions

#2-opt Local Search Heuristic
def twoOptHeurisct(route):
    route_len =  len(route)
    for i in range(route_len-1):
        for j in range(route_len-1):
            if(isNeighborhood2opt(i, j, route) == True): 
                if(i<j): swap2opt(route, i, j)
                elif(i>j): swap2opt(route, j, i)
    return route

#isNeighborhood2opt:
#considering 4 points A->B and D->E
#when  A->B + D->E > A->D + B->E then it is a legal move = local improvement
def isNeighborhood2opt(i, j, route):
    #intersectNode = (i!=j and (i<=j-2 or i>=j+2) and intersect(points[solution[i]], points[solution[i+1]], points[solution[j]], points[solution[j+1]]))
    improve = isImprovement(i, j, route)
    return improve

def isImprovement(i, j, route):
    actual = functions.length(route[i], route[i+1]) +  functions.length(route[j], route[j+1])
    new = functions.length(route[i], route[j]) +  functions.length(route[i+1], route[j+1]) 
    return new < actual

# A->B->C->D->E (A->B ..... D->E)
# A->D->C->B->E (A->D-> reverse(......) ->B->E)
def swap2opt(route, start, end):
    route[start+1:end+1] = reversed(route[start+1:end+1])