import functions
import random
class Individual:
    def __init__(self, customers, vehicle_count, vehicle_capacity):
        self.vehicle_tours = []
        self.customers = customers
        self.vehicle_count = vehicle_count
        self.vehicle_capacities = [vehicle_capacity] * vehicle_count
        self.vehicle_capacity = vehicle_capacity
        self.distance = 0
        self.fitness= 0.0
        self.selected = [0] * len(customers)
        
        for i in range(vehicle_count): 
            self.vehicle_tours.append([])
            self.vehicle_tours[i].append(customers[0])
            self.selected[0] = 1
    
    def routeDistance(self):
        if self.distance ==0:
            self.distance = functions.tourLen(self.vehicle_tours, self.vehicle_count, self.customers[0])
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness
    
    def addItemRoute(self, vehicle_id, customer):
        newcapacity = self.vehicle_capacities[vehicle_id] - customer.demand
        
        if(newcapacity >= 0): 
            self.vehicle_capacities[vehicle_id] = newcapacity
            self.vehicle_tours[vehicle_id].append(customer)
            self.selected[customer.index] = 1
            return True
        else: return False
        
    def swap(self, swappedC, swappedK, swapWithC, swapWithK):
        c1 = self.vehicle_tours[swappedK][swappedC]
        c2 = self.vehicle_tours[swapWithK][swapWithC]
        
        k1 = self.vehicle_capacities[swappedK] - c2.demand + c1.demand
        k2 = self.vehicle_capacities[swapWithK] - c1.demand + c2.demand
        
        if(k1 < 0 or k2 < 0 ): return False

        self.vehicle_tours[swappedK][swappedC] = c2
        self.vehicle_tours[swapWithK][swapWithC] = c1
        self.vehicle_capacities[swappedK] = k1
        self.vehicle_capacities[swapWithK] = k2
        return True
    
    def resetDistanceCalcultion(self):
        self.distance = 0
        self.fitness= 0.0
        
    #inner swap
    def innerSwap(self, index_v, index_c):
        swap = False
        route = self.vehicle_tours[index_v]
        route_len = len(route)
        if(index_c < route_len-1 and index_c>=1):
            for index_c2 in range(1, route_len-1):
                if(self.isInnerSwapImprovement(index_c, index_c2, route) == True): 
                    if(index_c<index_c2): self.innerSwapItem(route, index_c, index_c2)
                    elif(index_c>index_c2): self.innerSwapItem(route, index_c2, index_c)
                    swap = True
        if(swap): self.resetDistanceCalcultion()

    def isInnerSwapImprovement(self, i, j, route):
        actual = functions.length(route[i], route[i+1]) +  functions.length(route[j], route[j+1])
        new = functions.length(route[i], route[j]) +  functions.length(route[i+1], route[j+1])
        return new < actual

    # A->B->C->D->E (A->B ..... D->E)
    # A->D->C->B->E (A->D-> reverse(......) ->B->E)
    def innerSwapItem(self, route, start, end):
        route[start+1:end+1] = reversed(route[start+1:end+1])
        
    #outer swap
    def outerSwap(self, index_v, index_c):
        swap = False
        index_v2 = index_v
        while index_v2 == index_v: index_v2 = random.randint(0,len(self.vehicle_tours)-1)
        route1 = self.vehicle_tours[index_v]
        route2 = self.vehicle_tours[index_v2]
        route2_len = len(route2)
        for index_c2 in range(1, route2_len-1):
            if(self.isOuterSwapImprovement(index_c, index_c2, route1, route2) == True): 
                self.swap(index_c, index_v, index_c2, index_v2)
                swap = True
        if(swap): self.resetDistanceCalcultion()

    def isOuterSwapImprovement(self, index__c1, index__c2, route1, route2):
        actualr1 = functions.length(route1[index__c1-1], route1[index__c1]) +  functions.length(route1[index__c1], route1[index__c1+1])
        newr1 = functions.length(route1[index__c1-1], route2[index__c2]) +  functions.length(route2[index__c2], route1[index__c1+1])
        actualr2 = functions.length(route2[index__c2-1], route2[index__c2]) +  functions.length(route2[index__c2], route2[index__c2+1])
        newr2 = functions.length(route2[index__c2-1], route1[index__c1]) +  functions.length(route1[index__c1], route2[index__c2+1])
        return (newr1 < actualr1 and newr2 < actualr2)

    def testConstraints(self, name):
        self.selected = [0] * len(self.customers)
        self.vehicle_capacities = [self.vehicle_capacity] * self.vehicle_count
        v_index = 0
        for tour in self.vehicle_tours:
            for c in tour:
                if(self.selected[c.index] == 1 and c.index != 0): 
                    print (name + " customer" + str(c.index) + " is repeated")
                if(self.vehicle_capacities[v_index] - c.demand < 0): 
                    print (name + " capacity " + str(v_index) + " is " + str((self.vehicle_capacities[v_index] - c.demand)))                
                self.vehicle_capacities[v_index] -= c.demand
                self.selected[c.index] = self.selected[c.index] + 1
            v_index = v_index + 1
        if(self.selected[0] != self.vehicle_count*2): 
            print (name + " The number of customer 0 need to be " + str(self.vehicle_count*2) + ".")
        if (min(self.selected) == 0): 
            print (name + " Missing customers" + str(self.selected))
            
        