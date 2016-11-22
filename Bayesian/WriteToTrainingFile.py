import glob
from collections import Counter
import re
import enchant

DEFAULT_PATH = "/Users/preetipatel/PycharmProjects/SpamClassifier"
SPAM_BOOLEAN = "SPAM"
NONSPAM_BOOLEAN = "HAM"

words_ignore_list = ['','\n','the','to','a','an','some','we','i','you','he','she','it','they',
                     'and','of','for','our','your','be','with','is','are','this','that','in','will',
                     'at','from']

regex = re.compile('[^a-zA-Z]')
dictionary = enchant.DictWithPWL("en_US","mywords.txt")
frequency_dictionary = dict()

spam_filelist = glob.glob(DEFAULT_PATH + "/Spam Emails/*.txt")
nonspam_filelist = glob.glob(DEFAULT_PATH + "/NonSpam Emails/*.txt")

target = open(DEFAULT_PATH + "/Training Data/training_data.txt",'w')
word_frequency_target = open(DEFAULT_PATH + "/Training Data/words_frequency.txt",'w')

def formatWord(word):
    word = word.lower()
    word = word.rstrip()
    word = regex.sub('', word)

    return word

def writeToTrainingdata(list, spam_boolean):

    word_list = []
    number_of_emails = len(list)

    for file in list:
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
                        word_list.append(word)
                body_length = body_length + len(line)
        target.write(str(subject_length) + "," + str(body_length-subject_length) + "," + str(spelling_errors) + "," +spam_boolean + "\n")

    newList = Counter(word_list)
    sorted_list = sorted(newList.items(), key=lambda x: x[1], reverse=True)
    words_in_tuple = [x[0] for x in sorted_list]
    frequency_of_words = [x[1] for x in sorted_list]

    for i in range(len(words_in_tuple)):
        spamicity = float(frequency_of_words[i] / number_of_emails)
        word_frequency_target.write(words_in_tuple[i] + "," + str(spamicity) + "," + spam_boolean +"\n")

writeToTrainingdata(spam_filelist, SPAM_BOOLEAN)
writeToTrainingdata(nonspam_filelist, NONSPAM_BOOLEAN)

