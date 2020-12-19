
import functions
import nearestNeighbourAlgorithm

def twoOptHeurisct(points, nodeCount):
    solution = nearestNeighbourAlgorithm.nearestNeighbourAlgorithm(points, nodeCount)

    for i in range(nodeCount-1):
        for j in range(nodeCount-1):
            if(isNeighborhood2opt(i, j, points, solution) == True): 

                #print("A="+str(i)+"|,"+str(points[solution[i]].x)+","+str(points[solution[i]].y)+" B="+str(i+1)+"|,"+str(points[solution[i+1]].y)+","+str(points[solution[i+1]].y)+" C="+str(j)+"|,"+str(points[solution[j]].x)+","+str(points[solution[j]].y)+" D="+str(j+1)+"|,"+str(points[solution[j+1]].x)+","+str(points[solution[j+1]].y))
                #plot(solution, points, nodeCount)

                if(i<j): swap2opt(solution, i, j)
                elif(i>j): swap2opt(solution, j, i)


    if(functions.__PLOT): functions.plot(solution, points, nodeCount)
    return solution

def isNeighborhood2opt(i, j, points, solution):
    #intersectNode = (i!=j and (i<=j-2 or i>=j+2) and intersect(points[solution[i]], points[solution[i+1]], points[solution[j]], points[solution[j+1]]))
    improve = isImprovement(i, j, points, solution)
    return improve

def isImprovement(i, j, points, solution):
    actual = functions.length(points[solution[i]], points[solution[i+1]]) +  functions.length(points[solution[j]], points[solution[j+1]])
    new = functions.length(points[solution[i]], points[solution[j]]) +  functions.length(points[solution[i+1]], points[solution[j+1]])
    return new < actual

def swap2opt(solution, start, end):
    solution[start+1:end+1] = reversed(solution[start+1:end+1])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)