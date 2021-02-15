import functions
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

class Individual:
    def __init__(self, tour, customers, vehicle_count, vehicle_remaning_capacity):
        self.tour = tour
        self.customers = customers
        self.vehicle_count = vehicle_count
        self.vehicle_remaning_capacity = vehicle_remaning_capacity
        self.array_rep = [-1] * len(customers)
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            self.distance = functions.tourLen(self.tour, self.vehicle_count, self.customers[0])
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness
    
    def addItemRoute(vehicle, )

def geneticAlgorithmPlot(customers, vehicle_count, vehicle_capacity, popSize, eliteSize, mutationRate, generations):
    population = initialPopulation(popSize, customers, vehicle_count, vehicle_capacity)
    progress = []
    progress.append(1 / rankRoutes(population, customers, vehicle_count)[0][1])
    
    for i in range(0, generations):
        population = nextGeneration(population, customers, eliteSize, mutationRate, vehicle_count)
        progress.append(1 / rankRoutes(population, customers, vehicle_count)[0][1])
    
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()

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
    
    array_rep = 
    vehicle_tours = []
    vehicle_capacities = []
    
    for i in range(vehicle_count):
        vehicle_tours.append([])
        vehicle_capacities.append(vehicle_capacity)
        vehicle_tours[i].append(customers[0])
        
                
    while(len(customerscopy)>=2):
        nextCustomer = customerscopy.pop(random.randint(1, len(customerscopy)-1))
        
        dontHaveSpace = []
        for c in vehicle_capacities: dontHaveSpace.append(c < nextCustomer.demand)
        while(all(dontHaveSpace)): return None
            
        
        finish = False
        while(not finish):
            nextVehicle = int(random.random() * vehicle_count)
            if(vehicle_capacities[nextVehicle] >= nextCustomer.demand):
                vehicle_capacities[nextVehicle] -= nextCustomer.demand
                vehicle_tours[nextVehicle].append(nextCustomer)
                array_rep[nextCustomer.Index] = nextVehicle
                finish = True
    
    return Fitness(vehicle_tours, customers, vehicle_count, vehicle_capacities)
    
def swap(vehicle_tours, vehicle_capacity):
    return None
    #return [item for item in sequence if item < value]

def nextGeneration(currentGen, customers, eliteSize, mutationRate, vehicle_count):
    popRanked = rankRoutes(currentGen, customers, vehicle_count)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration



#Rank population
def rankRoutes(population, customers, vehicle_count):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i], customers, vehicle_count).routeFitness()
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

# Ordered crossover: we randomly select a subset of the first parent string and 
# then fill the remainder of the route with the genes from the second parent in the order in which they appear, 
# without duplicating any genes in the selected subset from the first parent
# Ex:
# parent 1 = 1 2 3 4 5 6 7 8 9
# parent 2 = 9 8 7 6 5 4 3 2 1
# offprint = 9 5 4 3 2 6 7 8 9
def breed(parent1, parent2, vehicle_count):
   
    child = []
    
    child.append[parent[0]]
    
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

def toursToRoute(tours):
    completeRoute = []
    for route in tours:
        for e in route: 
            if (e.index != 0): completeRoute.append(e)
    return completeRoute

def routeToTours(route, vehicle_capacity, vehicle_count):
    i = 0
    

#for each individual in population 
    # for each gene
        # with a probability "mutationRate" swap the gene with a random gene
def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual
