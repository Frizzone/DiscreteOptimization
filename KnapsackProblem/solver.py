#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])
maxValue = 0

DimVector = namedtuple('DimVector', ['init', 'end', 'totalValue','items'])

def greedy_algorithm(items, taken, capacity):
    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0

    items.sort(key = lambda x: (x.weight/x.value))

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value

def exhaustive_search(items, n, room):

    if(n>=len(items)):
        result = (0, ())
    elif(room - items[n].weight<0): 
        result = exhaustive_search(items, n+1, room)
    else: 
        withVal, withToTake = exhaustive_search(items, n+1, room - items[n].weight)
        withoutVal, withoutToTake = exhaustive_search(items, n+1, room)
        withVal += items[n].value

        if withVal > withoutVal:
            result = (withVal, withToTake + (items[n],))
        else:
            result = (withoutVal, withoutToTake)
    
    return result

def branch_bound(items, n, room):
    global maxValue
    if(n>=len(items)):
        result = (0, ())
        #bound
    elif(maxValue > relaxationFun2(items[n:], room)):
        result = (0, ())
    elif(room - items[n].weight<0):
        #left branch
        result = branch_bound(items, n+1, room)
    else:
        #left branch
        withVal, withToTake = branch_bound(items, n+1, room - items[n].weight)
        withVal += items[n].value

        #right branch
        withoutVal, withoutToTake = branch_bound(items, n+1, room)

        if withVal > withoutVal:
            result = (withVal, withToTake + (items[n],))
            maxValue = max(maxValue, withVal)   
        else:
            result = (withoutVal, withoutToTake)
            maxValue = max(maxValue, withoutVal) 

     
    return result

def relaxationFun1(items, capacity):
    return sum(item.value for item in items)

def relaxationFun2(items, capacity):
    items.sort(key = lambda x: (x.value/x.weight))
    value = 0
    weight = 0

    #print("capacity= " + str(capacity))
    for item in items:
        if weight + item.weight <= capacity:
            value += item.value
            weight += item.weight
            #print('+1 ->  v=' + str(item.value) + ' w=' + str(item.weight) + ' r='+ str(item.value/item.weight) + ' then totalWeight=' + str(weight) + ' total value='+ str(value))
        else:
            fraction = (capacity - weight) / item.weight
            weight += math.ceil(item.weight*fraction)
            value += math.ceil(item.value*fraction)
            #print("+f = " + str(fraction) + ' v=' + str(item.value*fraction) + ' w=' + str(item.weight) + ' then totalWeight=' + str(weight)  + ' total value='+ str(value))
            break
        
    return value


def log(n, value, room, estimate, maxvalue):
        print ('n =' + str(n) 
        + '/ value =' + str(value)
        + '/ room =' + str(room)
        + '/ estimate =' + str(estimate)
        + '/ maxValue =' + str(maxValue))

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    #print(input_data)

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    taken = [0]*len(items)
    #value = greedy_algorithm(items, taken, capacity)
    #value, toTake = exhaustive_search(items, 0, capacity)
    items.sort(key = lambda x: (x.weight/x.value))
    value, toTake = branch_bound(items, 0, capacity)


    for i in toTake: taken[i.index] = 1
 
    
    #value = greedy_algorithm(items, taken, capacity)

    #value2=0
    #for i in range(len(items)):
    #    value2 = value2 + taken[items[i].index]*items[i].value
    #   weight2 = weight2 + taken[items[i].index]*items[i].weight
    #print(str(value2) + ' ' + str(weight2))

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

