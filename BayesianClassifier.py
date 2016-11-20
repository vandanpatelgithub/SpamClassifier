from collections import Counter
import enchant
import re

list1 = ["apple","egg","apple","banana","egg","apple"]
newList = Counter(list1)
newList.most_common(3)

sorted_list = sorted(newList.items(), key = lambda x: x[1], reverse = True)


d = enchant.Dict("en_US")
print(d.check("November"))

word = "vandan12"
regex = re.compile('[^a-zA-Z]')
word = regex.sub('',word)
print(word)


