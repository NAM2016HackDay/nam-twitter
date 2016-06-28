import sys
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

corpus = parse_dictionary("thesaurus.txt")
xkcd = parse_list("trump-dict.txt")

#print xkcd[0:10]

#print str(sys.argv[1])

words = sys.argv[1].split()
for word in words:
    if not word in xkcd:
       try:
          sub_list = dictionary.synonym(word)#corpus[word]
	  
	  for item in sub_list:
	     if item in xkcd:
	     	#print "{} -> {}".format(word, item)
		print item, 
		word = item
		break
       except:
		#print "No subs for {}".format(word)
		print word,
    else:
	print word,
#print str.join(words)
#print words
#print corpus[sys.argv[1]][0]
