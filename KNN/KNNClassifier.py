import math
import operator

TRAINING_DATA = "/Users/preetipatel/PycharmProjects/SpamClassifier/Training Data/training_data.txt"
training_array = []
labels_array = []

def read_trainingfile(file):
    with open(file) as f:
        lines =  f.readlines()
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
            training_array.append(line[:-1])
            labels_array.append(line[-1])
    return training_array, labels_array

def euclideanDistance(instance1, instance2):
    distance = 0
    for x in range(len(instance1)):
        distance += pow(instance1[x] - instance2[x], 2)
    return math.sqrt(distance)

def getNeighbors(training_array, labels, testInstance, k):

    distances = []
    neighbors = []

    for x in range(len(training_array)):
        distance = euclideanDistance(testInstance, training_array[x])
        final_list = training_array[x] + [labels[x]]
        distances.append((final_list, distance))
    print("Distances before Sort : " + str(distances))
    distances.sort(key=operator.itemgetter(1))
    print("Distances after Sort : " + str(distances))

    for x in range(k):
        neighbors.append(distances[x][0])

    return neighbors

def convertToFloat(list):
    float_list = []
    for element in list:
        list = [float(i) for i in element]
        float_list.append(list)
    return float_list

training_array, labels_arrays = read_trainingfile(TRAINING_DATA)
float_list  = convertToFloat(training_array)
print("Float List : " + str(float_list))
#print("Training Data : " + str(training_array) + "\n" + "Labels : " + str(labels_array))
testInstance = [64.0, 487.0, 7.0]
neighbors = getNeighbors(float_list, labels_array, testInstance, 1)
print("Neighbors : " + str(neighbors[0][-1]))

