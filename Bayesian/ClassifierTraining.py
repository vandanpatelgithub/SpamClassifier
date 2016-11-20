import random
import math
import glob
import re

DEFAULT_PATH = "/Users/preetipatel/PycharmProjects/SpamClassifier/Training Data"
TRAINING_DATA = "/training_data.txt"
WORD_FREQUENCY = "/words_frequency.txt"

TESTING_EMAILS = "/Users/preetipatel/PycharmProjects/SpamClassifier/Testing Emails/*.txt"
testing_emails_list = glob.glob(TESTING_EMAILS)
regex = re.compile('[^a-zA-Z]')

words_ignore_list = ['', '\n', 'the', 'to', 'a', 'an', 'some', 'we', 'i', 'you', 'he', 'she', 'it', 'they',
                     'and', 'of', 'for', 'our', 'your', 'be', 'with', 'is', 'are', 'this', 'that', 'in', 'will',
                     'at', 'from']

dataset_list = []
spam_probability = dict()
ham_pribibility = dict()
final_spamicity = dict()

def loadTextFile(filename):
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(",")
            dataset = list(line)
            floats_dataset = [float(x) for x in dataset[:-1]]
            floats_dataset.append(dataset[-1].rstrip())
            dataset_list.append(floats_dataset)
    return dataset_list

def seperateByClass(dataset):
    separated = {}

    for i in range(len(dataset)):
        vector = dataset[i]
        if vector[-1] not in separated:
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated

def mean(numbers):
    return sum(numbers)/float(len(numbers))

def stddev(numbers):
    average = mean(numbers)
    variance = sum([pow(x-average,2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)

def summarize(dataset):
    summaries = [(mean(attribute), stddev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries

def summarizeByClass(dataset):
    separated = seperateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries

def calculateProbability(x, mean, stddev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stddev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stddev)) * exponent

def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities

def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel

dataset = loadTextFile(DEFAULT_PATH + TRAINING_DATA)
print("DATASET : " + str(dataset))
seperated = seperateByClass(dataset)
print("SEPARATED BY CLASS : " + str(seperated))

def readWordFrequency(file):

    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            list = line.split(",")
            key = list[0]
            spamicity = float(list[1])
            spam_boolean = list[2].rstrip()

            if spam_boolean == "SPAM":
                spam_probability[key] = spamicity
            elif spam_boolean == "HAM":
                ham_pribibility[key] = spamicity
    return spam_probability, ham_pribibility


def build_final_dictionary(spam_prob, ham_prob, file):

    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            list = line.split(",")
            word = list[0]

            if word in spam_prob and word in ham_prob:
                final_spamicity[word] = spam_prob[word] / (spam_prob[word] + ham_prob[word])
            elif word in spam_prob:
                final_spamicity[word] = spam_prob[word] / spam_prob[word]
            elif word in ham_prob:
                final_spamicity[word] = 0
    return final_spamicity

def combiningProbabilities(probabilities):

    multiply_prob = 1.0
    inverse_prob = 1.0

    for probability in probabilities:
        multiply_prob = multiply_prob * probability
        inverse_prob = inverse_prob * (1.0 - probability)

    if multiply_prob == 0 and inverse_prob == 0:
        combined_probability = 0
    else:
        combined_probability = float(multiply_prob / (multiply_prob + inverse_prob))

    return combined_probability

def final_probabilities(file_list):

    result_list = []
    for file in file_list:
        probability_list = []
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                words = line.split(" ")

                for word in words:
                    word = word.lower()
                    word = word.rstrip()
                    word = regex.sub('', word)
                    if word not in words_ignore_list:
                        if len(word) != 0 and len(word) < 15:
                            if word in final_spamicity:
                                print(word + " : " + str(final_spamicity[word]))
                                probability_list.append(final_spamicity[word])
        result = combiningProbabilities(probability_list)
        print(result)
        result_list.append(result)
    return result_list

def output(file_list):

    final_probs = final_probabilities(file_list)

    for i in range(len(file_list)):
        list = file_list[i].split("/")
        filename = list[-1]
        if final_probs[i] > 0.5:
            print(filename + " is SPAM")
        else:
            print(filename + " is HAM")



#spam, ham = readWordFrequency(DEFAULT_PATH+WORD_FREQUENCY)
#final_spamicity = build_final_dictionary(spam, ham, DEFAULT_PATH+WORD_FREQUENCY)
#print(final_spamicity)
#output(testing_emails_list)

#probabilities = [1.0,0]
#result  = combiningProbabilities(probabilities)
#print("Probabilities : " + str(result))





