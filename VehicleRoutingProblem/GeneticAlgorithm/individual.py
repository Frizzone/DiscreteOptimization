import functions

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
        
        k1 = self.vehicle_capacities[swappedK] + c2.demand - c1.demand
        k2 = self.vehicle_capacities[swapWithK] + c1.demand - c2.demand
        
        if(k1 < 0 or k2 < 0 ): return False

        
        self.vehicle_tours[swappedK][swappedC] = c2
        self.vehicle_tours[swapWithK][swapWithC] = c1
        self.vehicle_capacities[swappedK] = k1
        self.vehicle_capacities[swapWithK] = k2
        return True