import sys
import random
def parse_dictionary(file):
    myvars = {}
    with open(file) as myfile:
        for line in myfile:
            name, var = line.partition(":")[::2]
	    
            myvars[name.strip()] = var.split(',')
    return myvars

def parse_list(file):
    myvars = []
    with open(file) as myfile:
        for line in myfile:
	    
            myvars.append(line.rstrip())
	    
           #myvars[name.strip()] = var.split(',')
    return myvars

from PyDictionary import PyDictionary
dictionary=PyDictionary()

corpus = parse_dictionary("astro-sub.txt")

#print xkcd[0:10]

#print str(sys.argv[1])

words = sys.argv[1].split()
for i in xrange(len(words)):
    if words[i] in corpus:
          words[i] = random.choice(corpus[words[i]])

print words
