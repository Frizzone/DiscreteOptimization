import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt, math
import functions
import geneticAlgorithm.individual as ind
_PLOT_PROGRESS = True

def vpr_geneticAlgorithm(customers, vehicle_count, vehicle_capacity, popSize, eliteSize, mutationRate, generations):
    population = initialPopulation(popSize, customers, vehicle_count, vehicle_capacity)
    progress = []
    if(_PLOT_PROGRESS): 
        progress.append(1 / rankRoutes(population)[0][1])
    
    for i in range(0, generations):
        population = nextGeneration(population, eliteSize, mutationRate)
        if(_PLOT_PROGRESS): progress.append(1 / rankRoutes(population)[0][1])

    if(_PLOT_PROGRESS):  
        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()
    
    vehicle_tours = population[0].vehicle_tours
    population[0].testConstraints("Teste Final")
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
    remaining_customers = set(customers[1:])
    for v in range(0, vehicle_count):
        capacity_remaining = vehicle_capacity
        while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            shuffled_customers = list(remaining_customers)
            random.shuffle(shuffled_customers)
            for customer in shuffled_customers:
                if capacity_remaining >= customer.demand:
                    capacity_remaining -= customer.demand
                    insert = individual.addItemRoute(v, customer)
                    if(not insert): print(str(customer.index))
                    used.add(customer)
            remaining_customers -= used
                
    for v_id in range(vehicle_count): individual.addItemRoute(v_id, customers[0])
    if(min(individual.selected)== 0): return None
    #individual.testConstraints("create")
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
    #child.testConstraints("breed")
    return child

#get a route, repeated customers will be replaced by the nearest customer
def breedRouteToChild(parent, child, vehicle_id):
    randomTour = int(random.random() * len(parent.vehicle_tours))
    for c in parent.vehicle_tours[randomTour]:
        if(c.index !=0 and child.selected[c.index]==0):
            child.addItemRoute(vehicle_id, c)
        else:
            c = functions.nearestNode(parent.customers, child.vehicle_tours[vehicle_id][-1], child.selected)
            if(c != None): child.addItemRoute(vehicle_id, c)
    
    finish = False        
    while(not finish):
        c = functions.nearestNode(parent.customers, child.vehicle_tours[vehicle_id][-1], child.selected)
        if(c == None): finish = True
        else: finish = not (child.addItemRoute(vehicle_id, c))
    
    child.addItemRoute(vehicle_id, child.customers[0])
        

#for each individual in population 
    # for each gene
        # with a probability "mutationRate" swap the gene with a random gene
def mutatePopulation(population, mutationRate):
    mutatedPop = []
    popRanked = rankRoutes(population)
    for ind in range(0, len(population)):
        if (ind == popRanked[0][0]): 
            mutatedPop.append(population[ind])
        else: 
            mutatedInd = mutate(population[ind], mutationRate)
            mutatedPop.append(mutatedInd)
    return mutatedPop

def mutate(individual, mutationRate):
    for swappedK in range(1, len(individual.vehicle_tours)):
        for swappedC in range(1, len(individual.vehicle_tours[swappedK])-1):
            if(random.random() < mutationRate):
                individual.outerSwap(swappedK, swappedC)
            if(random.random() < mutationRate):
                individual.innerSwap(swappedK, swappedC)
    #individual.testConstraints("mutate")
    return individual
          
def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)
