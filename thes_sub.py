import sys, re
import random
def parse_dictionary(file):
    myvars = {}
    with open(file) as myfile:
        for line in myfile:
            name, var = line.partition(":")[::2]
	    
            myvars[name.strip()] = var.rstrip()#.split(',')
    return myvars

def parse_list(file):
    myvars = []
    with open(file) as myfile:
        for line in myfile:
	    
            myvars.append(line.rstrip())
	    
           #myvars[name.strip()] = var.split(',')
    return myvars

def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
    #multiples = re.findall(r"\$(.*)\$",  text)
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    #ret = []
    # For each match, look-up corresponding value in dictionary
    #for text in multiples:
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 
    #return ret

    
astro_replace = parse_dictionary("astro-sub.txt")

my_string="Supernova is a funny word."
my_string = sys.argv[1]

for k, v in astro_replace.iteritems():
    my_string = my_string.lower().replace(k, v)

print my_string

