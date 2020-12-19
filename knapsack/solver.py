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

def dynamic_programming_slow(capacity, items):
    value = 0
    weight = 0

    matrix = [[[0 for x in range(2)] for x in range(len(items) + 1)] for x in range(capacity + 1)]


    for i in range(len(items)+1):
        currentItem = items[i-1]
        for k in range(capacity+1):
            if (matrix[k][i][1] == 0): matrix[k][i][1]=()

            if (i==0 or k==0): 
                #quando é zero, não tem nenhum item
                matrix[k][i][0]=0
                matrix[k][i][1]=()
            elif (currentItem.weight <= k): 
                if(currentItem.value + matrix[k-currentItem.weight][i-1][0]):
                    matrix[k][i][0] = matrix[k-currentItem.weight][i-1][0] + currentItem.value
                    matrix[k][i][1] = matrix[k-currentItem.weight][i-1][1] + (currentItem,)
                else:
                    matrix[k][i][0] = matrix[k][i-1][0]
                    matrix[k][i][1] = matrix[k][i-1][1]
            else: 
                matrix[k][i][0] = matrix[k][i-1][0]
                matrix[k][i][1] = matrix[k][i-1][1]

    return matrix[capacity][len(items)][0], matrix[capacity][len(items)][1]

def dynamic_programming(capacity, items):
    value = 0
    weight = 0

    matrix=[[]for x in range(len(items) + 1)]

    for i in range(len(items)+1):
        if(i==0): 
            #consider number itens ==0
            matrix[i].append(DimVector(0,capacity, 0, []))
        else: 
            k = 0
            r = 0
            currentItem = items[i-1]
            oldRange = None
            while k < capacity:

                if(r==0):
                    #se é o range 0, joga 0 até o item caber ou o o primeiro r do i-1
                    rangeMinusI = findRangeByK(matrix[i-1], k)
                    nextk = min(rangeMinusI.end, currentItem.weight-1)
                    matrix[i].append(DimVector(0, nextk, 0, []))
                else: 
                    rangeMinusI = findRangeByK(matrix[i-1], k)
                    rangeMinusW = findRangeByK(matrix[i-1], k-currentItem.weight)
                    
                    #próxima mudança é o menor valor entre i-1,k e i-1,k-w => ESTA LÓGICA ESTA INCORRETA
                    #nextk = rangeMinusI.end
                    #if rangeMinusW.end != 0: nextk = min(nextk, rangeMinusW.end)
                    #para o primeiro item, considerar o peso
                    #if(r==0):  nextk = min(nextk, currentItem.weight-1)

                    #atualiza o fim do antigo
                    initk = 0
                    if(oldRange != None): initk = oldRange.end + 1
                    
                    nextk = 0
                    if(currentItem.value + rangeMinusW.totalValue > rangeMinusI.totalValue):
                        # se (i,k) + (i-1,k-w) > (i-1,k) => (i,k) + (i-1,k-w)

                        #VALIDAR
                        if(initk<currentItem.weight and rangeMinusI.TotalValue !=0): nextk = max(currentItem.weight, rangeMinusI.end)
                        else: nextk = min(rangeMinusI.end, rangeMinusW.End + currentItem.weight)
                        
                        matrix[i].append(DimVector(initk, nextk, currentItem.value + rangeMinusW.totalValue, rangeMinusW.items + [currentItem]))
                    else:
                        # se (i,k) + (i-1,k-w) < (i-1,k) => put (i-1,k)
                        nextk = rangeMinusI.end
                        matrix[i].append(DimVector(initk, nextk, rangeMinusI.totalValue, rangeMinusI.items))

                oldRange = matrix[i][r]
                r = r + 1
                k = k + nextk
    return matrix[capacity][len(items)].totalValue, matrix[capacity][len(items)].items

                
def findRangeByK(ranges, k):
        for r in ranges:
            # k fora da matriz
            if(k<0): return (DimVector(k, k, 0, []))
            # k dentro da matriz
            elif(k>=r.init and k<=r.end): return r

def dynamic_programming_rec(capacity, items, n):
    if n==0 or capacity==0: return 0

    if(items[n-1].weight > capacity): return dynamic_programming_rec(capacity, items, n-1)
    else: return max(items[n-1].value + dynamic_programming_rec(capacity-items[n-1].weight, items, n-1), dynamic_programming_rec(capacity, items, n-1))

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
    value = dynamic_programming(capacity, items)
    #value = dynamic_programming_rec(capacity, items, len(items))
    #value, toTake = exhaustive_search(items, 0, capacity)
    #items.sort(key = lambda x: (x.weight/x.value))
    #value, toTake = branch_bound(items, 0, capacity)


    #for i in toTake: taken[i.index] = 1
 
    
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

