import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt, math
import functions
import GeneticAlgorithm.individual as ind
_PLOT_PROGRESS = True

def vpr_geneticAlgorithm(customers, vehicle_count, vehicle_capacity, popSize, eliteSize, mutationRate, generations):
    population = initialPopulation(popSize, customers, vehicle_count, vehicle_capacity)
    progress = []
    if(_PLOT_PROGRESS): progress.append(1 / rankRoutes(population)[0][1])
    
    for i in range(0, generations):
        population = nextGeneration(population, eliteSize, mutationRate)
        if(_PLOT_PROGRESS): progress.append(1 / rankRoutes(population)[0][1])

    if(_PLOT_PROGRESS):  
        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()
    
    vehicle_tours = population[0].vehicle_tours
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
    individual = ind.Individual(customers, vehicle_count, vehicle_capacity)
    customer_count = len(customers)
    remaining_customers = customers[1:].copy()
    random.shuffle(remaining_customers)
    for v in range(0, vehicle_count):
        capacity_remaining = vehicle_capacity
        while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
            index = 0
            for customer in remaining_customers:
                if capacity_remaining >= customer.demand:
                    capacity_remaining -= customer.demand
                    insert = individual.addItemRoute(v, customer)
                    remaining_customers.pop(index)
                    if(not insert): print(str(customer.index))
                index=index+1
                
    for v_id in range(vehicle_count): individual.addItemRoute(v_id, customers[0])
    if(min(individual.selected)== 0): return None
    return individual

def nextGeneration(currentGen, eliteSize, mutationRate):
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


#breed
#firts: get best route of the parents
#second: get elements of the parent route, if already added get the nearest customer
def breed(parent1, parent2):
    child = ind.Individual(parent1.customers, parent1.vehicle_count, parent1.vehicle_capacity)
        
    #get the best tour from parents
    (bestTour, bestLen) = functions.bestTour(parent1.vehicle_tours + parent2.vehicle_tours, parent1.customers[0])
    for c in bestTour: 
        if(c.index!=0): 
            child.addItemRoute(0, c)
    child.addItemRoute(0, parent1.customers[0])
    
    for vehicle_id in range(1, parent1.vehicle_count):
        randomParent = random.randint(0, 1)
        if(randomParent==0):
            breedRouteToChild(parent1, child, vehicle_id)
        else:
            breedRouteToChild(parent2, child, vehicle_id)
    
    if(min(child.selected) == 0): 
        return parent1
    return child

#get a route, repeated customers will be replaced by the nearest customer
def breedRouteToChild(parent, child, vehicle_id):
    randomTour = int(random.random() * len(parent.vehicle_tours))
    for c in parent.vehicle_tours[randomTour]:
        if(c.index !=0 and child.selected[c.index]==0):
            child.addItemRoute(vehicle_id, c)
        else:
            c = functions.nearestNode(parent.customers, child.vehicle_tours[vehicle_id][-1], child.selected)
            child.addItemRoute(vehicle_id, c)
    
    finish = False        
    while(not finish):
        c = functions.nearestNode(parent.customers, child.vehicle_tours[vehicle_id][-1], child.selected)
        if(c.index == 0): finish = True
        else: finish = not (child.addItemRoute(vehicle_id, c))
    
    child.addItemRoute(vehicle_id, child.customers[0])
        

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
        for swappedC in range(1, len(individual.vehicle_tours[swappedK])-1):
            if(random.random() < mutationRate):
                outerSwap(individual, swappedK, swappedC)
            if(random.random() < mutationRate):
                innerSwap(individual, swappedK, swappedC)
                
    return individual

#inner swap
def innerSwap(individual, index_v, index_c):
    swap = False
    route = individual.vehicle_tours[index_v]
    route_len = len(route)
    if(index_c < route_len-1 and index_c>=1):
        for index_c2 in range(1, route_len-1):
            if(isInnerSwapImprovement(index_c, index_c2, route) == True): 
                if(index_c<index_c2): innerSwapItem(route, index_c, index_c2)
                elif(index_c>index_c2): innerSwapItem(route, index_c2, index_c)
                swap = True
    if(swap): 
        individual.distance = 0
        individual.fitness= 0.0

def isInnerSwapImprovement(i, j, route):
    actual = length(route[i], route[i+1]) +  length(route[j], route[j+1])
    new = length(route[i], route[j]) +  length(route[i+1], route[j+1])
    return new < actual

# A->B->C->D->E (A->B ..... D->E)
# A->D->C->B->E (A->D-> reverse(......) ->B->E)
def innerSwapItem(solution, start, end):
    solution[start+1:end+1] = reversed(solution[start+1:end+1])
    
#outer swap
def outerSwap(individual, index_v, index_c):
    swap = False
    index_v2 = index_v
    while index_v2 == index_v: index_v2 = random.randint(0,len(individual.vehicle_tours)-1)
    route1 = individual.vehicle_tours[index_v]
    route2 = individual.vehicle_tours[index_v2]
    route2_len = len(route2)
    for index_c2 in range(1, route2_len-1):
        if(isOuterSwapImprovement(index_c, index_c2, route1, route2) == True): 
            individual.swap(index_c, index_v, index_c2, index_v2)
            swap = True
    if(swap): 
        individual.distance = 0
        individual.fitness= 0.0

def isOuterSwapImprovement(index__c1, index__c2, route1, route2):
    actual = length(route1[index__c1-1], route1[index__c1]) +  length(route1[index__c1], route1[index__c1+1])
    new = length(route1[index__c1-1], route2[index__c2]) +  length(route2[index__c2], route1[index__c1+1])
    return new < actual
          
def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)
