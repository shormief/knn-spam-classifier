import csv
import math
import operator

def readCSVFile (filename, setToFill=[]):
    dataset = []
    with open(filename) as csvDataFile:
        row = csv.reader(csvDataFile)
        dataset = list(row)
        for x in range(1, len(dataset)):
            # converting data to float
            for y in range(1, 59):
                dataset[x][y] = float(dataset[x][y])
            setToFill.append(dataset[x])
    return setToFill

def getAvg(trainingSet):
    # finding average 
    totalAverages = ['Avg']
    for col in range (1, 58):
        average = 0
        for row in range (len(trainingSet)):
            average += trainingSet[row][col]
        average = average / len(trainingSet)
        totalAverages.append(average)
    return totalAverages

def getStandardDev(trainingSet, totalAverages):
    # finding standard deviation
    standardDeviation = ['Standard Deviation']
    for col in range (1, 58):
        totalSum = 0
        for row in range (len(trainingSet)):
            sumOfAvgSquared = trainingSet[row][col] - totalAverages[col]
            sumOfAvgSquared *= sumOfAvgSquared
            totalSum += sumOfAvgSquared
        totalSum = totalSum / (len(trainingSet) - 1)
        totalSum = math.sqrt(totalSum)
        standardDeviation.append(totalSum)
    return standardDeviation

def applyingNormalization(dataset, averageSet, standardDevSet):
    for col in range(1, 58):
        for row in range(len(dataset)):
            result = dataset[row][col] - averageSet[col]
            result = result / standardDevSet[col]
            dataset[row][col] = result
    return dataset

def getTotalDistances (testSet, traningSet):
    totalDistances = [] # a set that holds all of the distances 
    for x in range(len(testSet)): # for each row in testSet
        distances = [] # a set that holds the distances for the particular row; to be appended to totalDistances 
        for y in range(len(trainingSet)): # for each row in trainingSet
            dist = 0
            for i in range(1, 58): # for each column
                dist += pow((trainingSet[y][i] - testSet[x][i]), 2)
            dist = math.sqrt(dist)
            distances.append((y, dist))
        # sorting distances
        distances.sort(key=operator.itemgetter(1)) 
        totalDistances.append(distances)
    return totalDistances
            
def getNeighbors(totalDistances, k):
    totalNeighbors = []
    for a in range(len(totalDistances)):
        kNeighbors = []
        for b in range(k):
            kNeighbors.append(totalDistances[a][b])
        totalNeighbors.append(kNeighbors)
    return totalNeighbors

def makingPredictions (neighbors, trainingSet, k):
    predictonSet = []
    k_half = k / 2 # to calculate majority
    for x in range(len(neighbors)):
        spamCount = 0
        for y in range(k):
            index = neighbors[x][y][0]
            if (trainingSet[index][58] == 1):
                spamCount += 1
        if (spamCount >= k_half):
            predictonSet.append(1)
        else :
            predictonSet.append(0)
    # print(predictonSet)
    return predictonSet

def getAccuracy(testSet, predictionsSet):
    numCorrect = 0 
    for x in range(len(predictionsSet)):
        if predictionsSet[x] == testSet[x][58]:
            numCorrect += 1
    accuracy = numCorrect / float(len(testSet))
    return accuracy * 100.0

# initializing the sets
trainingSet = []
testSet = []

# filling the datasets w/ the data
trainingSet = readCSVFile("spam_train.csv", trainingSet)
averageSet = getAvg(trainingSet)
standardDevSet = getStandardDev(trainingSet, averageSet)
testSet = readCSVFile("spam_test.csv", testSet)
trainingSet = applyingNormalization(trainingSet, averageSet, standardDevSet)
testSet = applyingNormalization(testSet, averageSet, standardDevSet)
totalDistances = getTotalDistances(testSet, trainingSet)

# all the k-values to test 
k = [1, 5, 11, 21, 41, 61, 81, 101, 201, 401] 
for i in range(len(k)):
    neighbors = getNeighbors(totalDistances, k[i])
    predictionSet = makingPredictions(neighbors, trainingSet, k[i])
    accuracy = getAccuracy(testSet, predictionSet)
    print(str(k[i]) + ": " + str(accuracy))

