import functions
from enum import Enum
import nearestNeighbourAlgorithm


class OptCase(Enum):
    #A->B  C->D   E->F
    opt_case_1 = 0 #A->D  E->C  B->F
    opt_case_2 = 1 #A->E  D->B  C->F
    opt_case_3 = 2 #A->C  B->E  D->F
    opt_case_4 = 3 #A->D  E->B  C->F
    opt_case_5 = 4 #A->C  B->D  E->F
    opt_case_6 = 5 #A->E  D->C  B->F
    opt_case_7 = 6 #A->B  C->E  D->F

def threeOptHeurisct(points, nodeCount):
    solution = nearestNeighbourAlgorithm.nearestNeighbourAlgorithm(points, nodeCount)
    functions.plot(solution, points, nodeCount)

    for i in range(nodeCount-2):
        for j in range(nodeCount-2):
            for l in range(nodeCount-2):
                if(i!=j and j!=l and i!=l and i!=j+1 and j!=l+1 and i!=j+1): 
                    bestSwap = bestNeighborhood3opt(i, j, l, points, solution)
                    if(bestSwap>0): solution = swap3opt(solution, i, j, l, bestSwap)
    
    functions.plot(solution, points, nodeCount)
    return solution

def bestNeighborhood3opt(i, j, l, points, solution):
    indexList = [i, j, l]
    indexList.sort()
    
    A = points[solution[indexList[0]]]
    B = points[solution[indexList[0]+1]]
    C = points[solution[indexList[1]]]
    D = points[solution[indexList[0]+1]] 
    E = points[solution[indexList[2]]]
    F = points[solution[indexList[2]+1]]

    actual = functions.length(A, B) +  functions.length(C, D) + functions.length(E, F) 

    cases = []
    cases.append(functions.length(A, D) +  functions.length(E, C) + functions.length(B, F))
    cases.append(functions.length(A, E) +  functions.length(D, B) + functions.length(C, F))
    cases.append(functions.length(A, C) +  functions.length(B, E) + functions.length(D, F))
    cases.append(functions.length(A, D) +  functions.length(E, B) + functions.length(C, F))
    cases.append(functions.length(A, C) +  functions.length(B, D) + functions.length(E, F))
    cases.append(functions.length(A, E) +  functions.length(D, C) + functions.length(B, F))
    cases.append(functions.length(A, B) +  functions.length(C, E) + functions.length(D, F))

    if(min(cases) < actual): return cases.index(min(cases))
    else: return -1

def swap3opt(solution, i, j, l, bestSwap):
    indexList = [i, j, l]
    indexList.sort()

    A = indexList[0]
    B = A+1
    C = indexList[1]
    D = C+1 
    E = indexList[2]
    F = E+1

    sA = solution[0:A+1]
    sBC = solution[B:C+1]
    sDE = solution[D:E+1]
    sF = solution[F:-1]

    newSolution = []

    if(bestSwap == OptCase.opt_case_1.value): newSolution = sA + sDE + list(reversed(sBC)) + sF
    elif(bestSwap == OptCase.opt_case_2.value): newSolution = sA + list(reversed(sDE)) + sBC + sF
    elif(bestSwap == OptCase.opt_case_3.value): newSolution = sA + list(reversed(sBC)) + list(reversed(sDE)) + sF
    elif(bestSwap == OptCase.opt_case_4.value): newSolution = sA + sDE + sBC + sF
    elif(bestSwap == OptCase.opt_case_5.value): newSolution = sA + list(reversed(sBC)) + sDE + sF
    elif(bestSwap == OptCase.opt_case_6.value): newSolution = sA + list(reversed(sDE)) + list(reversed(sBC)) + sF
    elif(bestSwap == OptCase.opt_case_7.value): newSolution = sA + sBC + list(reversed(sDE)) + sF

    return newSolution
