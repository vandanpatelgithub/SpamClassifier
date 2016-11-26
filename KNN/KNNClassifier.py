import math
import operator
import glob
import re
import enchant

TRAINING_DATA = "/Users/preetipatel/PycharmProjects/SpamClassifier/Training Data/training_data.txt"
TESTING_EMAILS = "/Users/preetipatel/PycharmProjects/SpamClassifier/Testing Emails/*.txt"
testing_emails_list = glob.glob(TESTING_EMAILS)
training_array = []
labels_array = []

words_ignore_list = ['', '\n', 'the', 'to', 'a', 'an', 'some', 'we', 'i', 'you', 'he', 'she', 'it', 'they',
                     'and', 'of', 'for', 'our', 'your', 'be', 'with', 'is', 'are', 'this', 'that', 'in', 'will',
                     'at', 'from']

regex = re.compile('[^a-zA-Z]')
dictionary = enchant.DictWithPWL("en_US","mywords.txt")

def read_trainingfile(file):
    with open(file) as f:
        lines =  f.readlines()
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
            training_array.append(line[:-1])
            labels_array.append(line[-1])
    return training_array, labels_array

def formatWord(word):
    word = word.lower()
    word = word.rstrip()
    word = regex.sub('', word)

    return word

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
    #print("Distances before Sort : " + str(distances))
    distances.sort(key=operator.itemgetter(1))
    #print("Distances after Sort : " + str(distances))

    for x in range(k):
        neighbors.append(distances[x][0])

    return neighbors

def getResponse(neighbors):
    classVotes = {}

    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1

    sortedVotes = sorted(classVotes.items(), key = operator.itemgetter(1), reverse = True)

    return sortedVotes[0][0]

def convertToFloat(list):
    float_list = []
    for element in list:
        list = [float(i) for i in element]
        float_list.append(list)
    return float_list

def testInstances(file_list):
    testInstance = []
    for file in file_list:
        body_length = 0
        spelling_errors = 0
        with open(file) as f:
            lines = f.readlines()
            subject_length = len(lines[0].rstrip())

            for line in lines:
                words = line.split(" ")
                for word in words:
                    word = formatWord(word)
                    word_length = len(word)
                    if word not in words_ignore_list and word_length != 0 and word_length < 15:
                        if not dictionary.check(word.title()):
                            spelling_errors = spelling_errors + 1
                body_length = body_length + len(line)
            body_length = body_length - subject_length
        testInstance.append([float(subject_length), float(body_length), float(spelling_errors)])
    return testInstance


training_array, labels_arrays = read_trainingfile(TRAINING_DATA)
float_list  = convertToFloat(training_array)
#print("Float List : " + str(float_list))
testInstance = testInstances(testing_emails_list)
#print("Test Instance : " + str(testInstance))
for instance in testInstance:
    neighbors = getNeighbors(float_list, labels_array, instance, 1)
    response = getResponse(neighbors)
    print("Response : " + response)
#print("Training Data : " + str(training_array) + "\n" + "Labels : " + str(labels_array))
#testInstance = [64.0, 487.0, 7.0]
#neighbors = getNeighbors(float_list, labels_array, testInstance, 2)
#print("Neighbors : " + str(neighbors))
#response = getResponse(neighbors)
#print("Response : " + response)

