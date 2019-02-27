'''
Notes:
Sample Chromosome = [1,2,4,65,12,51,42,....32] // length = 194
'''
from random import *
import math
import heapq #finding nth largest
import matplotlib.pyplot as plt
import numpy as np

# helper functions
def generateRandomChromosome(): 
    chro = []
    start = 0
    for i in range (0,194):
        #generate random number
        randNo = randint(1, 194)
        if(len(chro)==0):
            start = randNo
        while randNo in chro:
            randNo = randint(1, 194)
        chro.append(randNo)
    return(chro) #length 195

def getFitnessOfChromo(chromo, data): #doesnt show distance
    total = getDistFromCity(chromo[0], chromo[1], data)
    for i in range (2, 194):
        total = total + getDistFromCity(chromo[i-1],chromo[i], data)
    total = total + getDistFromCity(chromo[-1],chromo[0], data)
    total = 1000000000/total
    return(total) #the less the total the greater the fitness

def getFitnessAsDistance(chromo, data): #doesnt show distance
    total = getDistFromCity(chromo[0], chromo[1], data)
    for i in range (2, 194):
        total = total + getDistFromCity(chromo[i-1],chromo[i], data)
    total = total + getDistFromCity(chromo[-1],chromo[0], data)
    return(total) #the less the total the greater the fitness

def generateRandomPopulation(size): # generates Population size: 30
    population = []
    for i in range (0,size):
        population.insert(i,generateRandomChromosome())
    return(population)

def readData():
    f = open("data.txt", "r")
    coods = []
    i=0
    for x in f:
        #extract parts
        parts= []
        temp = ""
        for j in x:
            if((j==' ')or(j=='\n')):
                parts.append(temp)
                temp = ""
            else:
                temp = temp + str(j);
        coods.insert(i,parts)
        i=i+1
    return(coods)

def getCoodsFromCity(cityNumber, data):
    return [data[cityNumber-1][1],data[cityNumber-1][2]]

def getDistFromCity(cityNumber1, cityNumber2, data):
    cityCoods1 = getCoodsFromCity(cityNumber1, data)
    cityCoods2 = getCoodsFromCity(cityNumber2, data)
    return (math.sqrt((float(cityCoods1[0])-float(cityCoods2[0]))**2 + (float(cityCoods1[1])-float(cityCoods2[1]))**2))

#parent selection procedures

def fitnessProportionalSelection(fitness, nSelect):
    fitnessSum = 0
    fitnessProportions = []
    parentsIndices = []
    appendValue = 0
    for i in fitness:
        fitnessSum = fitnessSum + i
    for i in fitness:
        fitnessProportions.append(i/fitnessSum)
    #choosing parents
    for n in range (nSelect):
        findParentLoop = True
        if(len(parentsIndices)==len(fitness)):
            findParentLoop = False;
        while(findParentLoop == True):
            randNo = random()
            lower = 0
            for i in range (len(fitness)):
                if ((randNo>lower) and (randNo<lower + fitnessProportions[i])):
                    if(i not in parentsIndices):
                        parentsIndices.append(i)
                        findParentLoop = False
                lower = lower + fitnessProportions[i]
    return parentsIndices

def nth_largest(n, iter):
    return heapq.nlargest(n, iter)[-1]

def rankbasedSelection(fitness, nSelect):
    rankSum = 0
    ranksProportion = []
    parentsIndices = []
    #creating array for storing ranks
    ranks = []
    for i in range (len(fitness)):
        ranks.append(0)
    #finding ranks
    for i in range (1,len(fitness)+1):
        nthLargestElement = nth_largest(i, fitness)
        for j in range (len(fitness)):
            if (nthLargestElement == fitness[j]):
                ranks[j] = len(fitness)-i;
    # rank sum for calculation proportions
    
    for i in ranks:
        rankSum = rankSum + i
    for i in ranks:
        ranksProportion.append(i/rankSum)
    #choosing parents
    for n in range (nSelect):
        findParentLoop = True
        if(len(parentsIndices)==len(fitness)):
            findParentLoop = False;
        while(findParentLoop == True):
            randNo = random()
            lower = 0
            for i in range (len(fitness)):
                if ((randNo>lower) and (randNo<lower + ranksProportion[i])):
                    if(i not in parentsIndices):
                        parentsIndices.append(i)
                        findParentLoop = False
                lower = lower + ranksProportion[i]
    return parentsIndices

def randomSelection(fitness, nSelect):
    selectedIndex = []
    for i in range (nSelect):
        isChildComplete = False
        while(isChildComplete==False):
            randNo = randint(0, len(fitness)-1)
            if (randNo) not in selectedIndex:
                selectedIndex.append(randNo)
                isChildComplete = True;
    return selectedIndex

def truncation(fitness, nSelect):
    selectedIndex = []
    #finding ranks
    for i in range (1,nSelect+1):
        nthLargestElement = nth_largest(i, fitness)
        for j in range (len(fitness)):
            if (nthLargestElement == fitness[j]):
                selectedIndex.append(j)
                break
    #print(selectedIndex)
    return selectedIndex
        
    
def binaryTournament(fitness, nSelect):
    parentsIndices = []
    pool = []
    poolLoop = True
    poolBest = 0
    #players for pool1
    for n in range (nSelect):
        while (poolLoop):
            for i in range (2):
                randNo = randint(0, len(fitness)-1)
                if(len(parentsIndices)==len(fitness)-1):
                    poolLoop = False;
                if ((randNo not in parentsIndices) and (len(parentsIndices)<len(fitness)+1)):
                    if(len(pool)==1):
                        if (pool[0] != randNo):
                            pool.append(randNo)
                            poolLoop = False
                    if(len(pool)==0):
                        pool.append(randNo)
        #best from pool 1            
        if (len(pool)==2):
            # for parent select
            if(fitness[pool[0]]>fitness[pool[1]]):
                poolBest = pool[0];
            if(fitness[pool[0]]<fitness[pool[1]]):
                poolBest = pool[1];
            parentsIndices.append(poolBest)
                
        if (len(parentsIndices)<nSelect):
            poolLoop = True
            pool = []
            poolBest = 0
    return(parentsIndices)
    
    
def crossOver(parentsIndex, population):
    startCopyIndex = randint(1, 190)
    finishCopyIndex = randint(startCopyIndex, 193)
    #print(startCopyIndex, finishCopyIndex)
    
    parent1 = population[parentsIndex[0]]
    parent2 = population[parentsIndex[1]]
    producedChildren = []
    child1 = []
    child2 = []
    #generating template
    for i in range(194):
        child1.append(-222)
        child2.append(-222)
    #generating child
        
    # child 1
    child1[startCopyIndex:finishCopyIndex] = parent1[startCopyIndex:finishCopyIndex]
    isChildComplete = False;
    childIndex = finishCopyIndex
    ParentIndex = finishCopyIndex

    while(isChildComplete==False):
        if(parent2[ParentIndex] not in child1[startCopyIndex:finishCopyIndex]):
            child1[childIndex] = parent2[ParentIndex];
            childIndex+= 1
            ParentIndex+= 1
        elif (parent2[ParentIndex] in child1[startCopyIndex:finishCopyIndex]):
            ParentIndex+= 1
        if (ParentIndex==len(child1)):
            ParentIndex = 0
        if (childIndex==len(child1)):
            childIndex = 0
        if(childIndex == startCopyIndex):
            isChildComplete = True

    child2[startCopyIndex:finishCopyIndex] = parent2[startCopyIndex:finishCopyIndex]
    isChildComplete = False;
    childIndex = finishCopyIndex
    ParentIndex = finishCopyIndex
    while(isChildComplete==False):
        if(parent1[ParentIndex] not in child2[startCopyIndex:finishCopyIndex]):
            child2[childIndex] = parent1[ParentIndex];
            childIndex+= 1
            ParentIndex+= 1
        elif (parent1[ParentIndex] in child2[startCopyIndex:finishCopyIndex]):
            ParentIndex+= 1
        if (ParentIndex==len(child2)):
            ParentIndex = 0
        if (childIndex==len(child2)):
            childIndex = 0
        if(childIndex == startCopyIndex):
            isChildComplete = True

    #adding child
    producedChildren.append(child1)
    producedChildren.append(child2)
    return(producedChildren)        

def mutation(children, rate):
    mutatedChildren = children
    for i in range (len(mutatedChildren)):
        randNo = random()
        if (randNo<rate):
            # switching calues
            switchPos1 = randint(0, int(193/2))
            switchPos2 = randint(int(193/2), 192)
            temp = mutatedChildren[i][switchPos1]
            mutatedChildren[i][switchPos1] = mutatedChildren[i][switchPos2]
            mutatedChildren[i][switchPos2] = temp
    return mutatedChildren
        
#main

def plotGraph(nGenerations, avgArray, minArray):
    genArray = []
    for i in range (nGenerations):
        genArray.append(i)
    # red dashes, blue squares and green triangles
    plt.plot(genArray, avgArray,'r',genArray, minArray,'b')
    plt.show()


def main():
    averagePerGen = []
    minPerGen = []
    minTotal = 1000000000
    
    data = readData()
    # setting some variables
    nPopulation = 60
    mutationRate = 0.4
    nChildren = 10 #must be even
    nGenerations = 20000000000
    # generate initial population
    population = generateRandomPopulation(nPopulation)
    fitness = []
    fitnessDistance = []
    # compute fitness
    for i in population:
        fitness.append(getFitnessOfChromo(i, data))
        fitnessDistance.append(getFitnessAsDistance(i, data))
    #print("fitness:",fitness)
    # Population[3] has the fitness[3]

    #begin loop
    try:
        for generation in range (nGenerations):
            if(min(fitnessDistance)<minTotal):
                minTotal = min(fitnessDistance)
            averagePerGen.append(sum(fitnessDistance) / float(len(fitnessDistance)))
            minPerGen.append(minTotal)
            
            if(generation%100==0):
                print("generation:",generation)

                #fitness statistics
                print("distance (avg, min): ", sum(fitnessDistance) / float(len(fitnessDistance)), minTotal)
            
                
            for childGeneration in range (nChildren//2):
                # choosing parents 
                #parentsIndex = fitnessProportionalSelection(fitness, 2)
                #parentsIndex = rankbasedSelection(fitness, 2 )
                #parentsIndex = binaryTournament(fitness, 2)
                #parentsIndex = randomSelection(fitness, 2)
                parentsIndex = truncation(fitness, 2)
                
                
                children = crossOver(parentsIndex, population);
                children = mutation(children, mutationRate) #mutated children
            
                #compute fitness of children        
                for i in range (len(children)):
                    population.append(children[i])
                    fitness.append(getFitnessOfChromo(children[i], data))
                    fitnessDistance.append(getFitnessAsDistance(children[i], data))
                    
            # select new population        
            #populationIndices = fitnessProportionalSelection(fitness, nPopulation)
            #populationIndices = rankbasedSelection(fitness, nPopulation)
            #populationIndices = binaryTournament(fitness, nPopulation)
            #populationIndices = randomSelection(fitness, nPopulation)
            populationIndices = truncation(fitness, nPopulation)
            #print(len(populationIndices))

            tempPopulation = []
            tempFitness = []
            tempFitnessDistance = []
            for i in (populationIndices):
                tempFitness.append(fitness[i])
                tempFitnessDistance.append(fitnessDistance[i])
                tempPopulation.append(population[i])
                
            population = tempPopulation
            fitness = tempFitness
            fitnessDistance = tempFitnessDistance
        return [averagePerGen,minPerGen]
    except:
        print("mainPath", population[truncation(fitness, 1)[0]], "distance", minTotal)


    

#fullmain
def Fullmain():
    resultArray = []
    nIterations = 10
    avgAllIterations = []
    minAllIterations = []
    avg_avgAllIterations = []
    avg_minAllIterations = []
    '''
    avgAllIterations = [[12,3,412,3] //len gen, ...]//len 10
    '''
    for i in range (nIterations):
        resultArray = main()
        print("iteration,", i)
        avgAllIterations.append(resultArray[0]) # avg of all gen
        minAllIterations.append(resultArray[1]) # min of all gen

    #calculationg averages of avgAllIterations
    for i in range (200): #nGenearations
        sumAvgs = 0
        for j in range (nIterations):
            sumAvgs = sumAvgs + avgAllIterations[j][i]
        avg_avgAllIterations.append(sumAvgs / nIterations)

    #calculationg averages of minAllIterations
    for i in range (200): #nGenearations
        sumMin = 0
        for j in range (nIterations):
            sumMin = sumMin + minAllIterations[j][i]
        avg_minAllIterations.append(sumMin / nIterations)

    #collected data
    '''
    print("generation# Run#1.Average Run#2.Average Run#3.Average Run#4.Average Run#5.Average Run#6.Average Run#7.Average Run#8.Average Run#9.Average Run#10.Average Average.Average")
    for i in range (len(minAllIterations[0])):
        print(i , avgAllIterations[0][i],avgAllIterations[1][i],avgAllIterations[2][i],avgAllIterations[3][i],avgAllIterations[4][i],avgAllIterations[5][i],avgAllIterations[6][i],avgAllIterations[7][i],avgAllIterations[8][i],avgAllIterations[9][i],avg_avgAllIterations[i])

    print("")
    print("generation# Run#1.BFS Run#2.BFS Run#3.BFS Run#4.BFS Run#5.BFS Run#6.BFS Run#7.BFS Run#8.BFS Run#9.BFS Run#10.BFS Average.BFS")
    for i in range (len(minAllIterations[0])):
        print(i , minAllIterations[0][i],minAllIterations[1][i],minAllIterations[2][i],minAllIterations[3][i],minAllIterations[4][i],minAllIterations[5][i],minAllIterations[6][i],minAllIterations[7][i],minAllIterations[8][i],minAllIterations[9][i],avg_minAllIterations[i])
    '''
    plotGraph(len(avg_avgAllIterations),avg_avgAllIterations, avg_minAllIterations)


#Fullmain()
main()
