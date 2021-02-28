#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions
import localsearch.twoOptHeurisct as twoOptHeurisct
import localsearch.twoOptIterateLS as twoOptIterateLS
import localsearch.threeOptHeurisct as threeOptHeurisct
import visualization

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(functions.Point(float(parts[0]), float(parts[1])))


    option = input ("(1) 2-opt Local Search\n(2) 2-opt Iterated Local Search\n(3) 3-opt Local Search\n>>")
    
    solution = []
    if(option =="1"):
        solution = twoOptHeurisct.twoOptHeurisct(points, nodeCount)
    elif(option =="2"):
        timeout = int(input("Timeout in seconds:"))
        solution = twoOptIterateLS.twoOptIterateLS(points, nodeCount, timeout)
    elif(option =="3"):
        solution = threeOptHeurisct.threeOptHeurisct(points, nodeCount)
    
    if(visualization.__PLOT): visualization.plot(solution, points, nodeCount)

    # calculate the length of the tour
    obj = functions.tourLength(solution, points, nodeCount)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data











import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

