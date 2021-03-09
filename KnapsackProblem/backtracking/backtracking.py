import math
maxValue = 0

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