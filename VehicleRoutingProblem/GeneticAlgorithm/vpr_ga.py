import functions
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
_PLOT_PROGRESS = True
import twoOptHeurisct

class Individual:
    def __init__(self, customers, vehicle_count, vehicle_capacity):
        self.vehicle_tours = []
        self.customers = customers
        self.vehicle_count = vehicle_count
        self.vehicle_capacities = [vehicle_capacity] * vehicle_count
        self.vehicle_capacity = vehicle_capacity
        self.array_rep = [-1] * len(customers) * vehicle_count
        self.distance = 0
        self.fitness= 0.0
        
        for i in range(vehicle_count): 
            self.vehicle_tours.append([])
            self.vehicle_tours[i].append(customers[0])
            self.array_rep[i*(len(self.customers))] = 0
    
    def routeDistance(self):
        if self.distance ==0:
            self.distance = functions.tourLen(self.vehicle_tours, self.vehicle_count, self.customers[0])
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness
    
    def addItemRoute(self, vehicle_id, customer):
        self.vehicle_capacities[vehicle_id] -= customer.demand
        self.vehicle_tours[vehicle_id].append(customer)
        self.array_rep[customer.index + vehicle_id*(len(self.customers))] = customer.index
    
    def compress_array_rep(self):
        self.array_rep = [i for i in self.array_rep if i != -1]
        
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
    
    def search(c_index):
        for v in len(self.vehicle_tours):
            for c in  len(self.vehicle_tours[v]):
                if(self.vehicle_tours[c][v].index == c_index): return (v,c)
        return None

def vpr_geneticAlgorithm(customers, vehicle_count, vehicle_capacity, popSize, eliteSize, mutationRate, generations):
    population = initialPopulation(popSize, customers, vehicle_count, vehicle_capacity)
    progress = []
    if(_PLOT_PROGRESS): progress.append(1 / rankRoutes(population)[0][1])
    
    for i in range(0, generations):
        population = nextGeneration(population, customers, eliteSize, mutationRate, vehicle_count)
        if(_PLOT_PROGRESS): progress.append(1 / rankRoutes(population)[0][1])

    if(_PLOT_PROGRESS):  
        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()
    
    #busca local em cada veículo
    vehicle_tours = population[0].vehicle_tours
    for v in range(vehicle_count):
        vehicle_tours[v] = twoOptHeurisct.twoOptHeurisct(vehicle_tours[v],  customers, len(vehicle_tours[v]))
    
    
    return vehicle_tours

#Initial population
def initialPopulation(popSize, customers, vehicle_count, vehicle_capacity):
    population = []

    i=0
    while (i<= popSize):
        tours = createTours(customers, vehicle_count, vehicle_capacity)
        if (tours != None):
            population.append(tours)
            i = i+1
        
    return population

#Create random tours
def createTours(customers, vehicle_count, vehicle_capacity):
    customerscopy = customers.copy()
    individual = Individual(customers, vehicle_count, vehicle_capacity)

    while(len(customerscopy)>=2):
        nextCustomer = customerscopy.pop(random.randint(1, len(customerscopy)-1))
        
        dontHaveSpace = []
        for c in individual.vehicle_capacities: dontHaveSpace.append(c < nextCustomer.demand)
        while(all(dontHaveSpace)): return None
        
        finish = False
        while(not finish):
            nextVehicle = int(random.random() * vehicle_count)
            if(individual.vehicle_capacities[nextVehicle] >= nextCustomer.demand):
                individual.addItemRoute(nextVehicle, nextCustomer)
                finish = True
    individual.compress_array_rep()
    return individual

def nextGeneration(currentGen, customers, eliteSize, mutationRate, vehicle_count):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

#Rank population
def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = population[i].routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#Selection
#Elitism: select best routes
def selection(popRanked, eliteSize):
    selectionResults = []
    for i in range(0, len(popRanked)):
        selectionResults.append(popRanked[i][0])
        
    return selectionResults


#create a ordered array of individuals (population)
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

# breed Population and create a children population modified
def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    # the elite bests (elite) individuals (routes) in matingpool don't suffer crossover modification
    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    # the remaining worst: breed with random individuals (routes) in matingpool and create modified children
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children


# totally random crossover
def breed(parent1, parent2):
    customerscopy = parent1.customers.copy()
    child = Individual(parent1.customers, parent1.vehicle_count, parent1.vehicle_capacity)

    while(len(customerscopy)>=2):
        nextCustomer = customerscopy.pop(random.randint(1, len(customerscopy)-1))
        
        dontHaveSpace = []
        for c in child.vehicle_capacities: dontHaveSpace.append(c < nextCustomer.demand)
        while(all(dontHaveSpace)): return parent2
            
        finish = False
        while(not finish):
            nextVehicle = int(random.random() * parent1.vehicle_count)
            if(child.vehicle_capacities[nextVehicle] >= nextCustomer.demand):
                child.addItemRoute(nextVehicle, nextCustomer)
                finish = True
    child.compress_array_rep()
    
    return child

#for each individual in population 
    # for each gene
        # with a probability "mutationRate" swap the gene with a random gene
def mutatePopulation(population, mutationRate):
    #return population
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def mutate(individual, mutationRate):
    for swappedK in range(1, len(individual.vehicle_tours)):
        for swappedC in range(1, len(individual.vehicle_tours[swappedK])):
            if(random.random() < mutationRate):
                swapWithK = random.randint(1, len(individual.vehicle_tours)-1)
                swapWithC = random.randint(1, len(individual.vehicle_tours[swapWithK])-1)
                individual.swap(swappedC, swappedK, swapWithC, swapWithK)
            if(random.random() < mutationRate):
                twoOptHeurisct.partialInnerTwoOptHeurisct(individual.vehicle_tours[swappedK], swappedC,  individual.customers, len(individual.vehicle_tours[swappedK]))
                
    return individual
