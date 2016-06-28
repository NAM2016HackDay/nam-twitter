import tweepy
import arxiv
from credentials import *
import re

class Twitter():
    """
    An object to interact with the Twitter API in the simple way that we need.

    """
    def __init__(self):
        """
        Authenticates the Python script against the Twitter auth API, and
        sets up the object.
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, string):
        """
        Send a string to Twitter.
        """
        if len(string)>140:
            print "This string is too long, and it will be truncated to fit on Twitter."
            
        selt.api.update_status(string[:140])

class ArxivQuery():
    """
    Query the Arxiv for abstracts.
    """
        
    #s = "GW150914"
    
    def query(self):
        return arxiv.query(s, prune=True, start=0, max_results=10)

class Converter():
    """
    Convert a string into human-friendly format
    """

    def __init__(self):
        self.astro_replace = self.parse_dictionary("astro-sub.txt")
        print self.astro_replace

    def sub(self, string):
        return self.multiple_replace(self.astro_replace, string)

    def parse_dictionary(self, file):
        myvars = {}
        with open(file) as myfile:
            for line in myfile:
                name, var = line.partition(":")[::2]
                myvars[name.strip()] = " ".join(var.rsplit())
        return myvars
            
    def multiple_replace(self, dict, text):
        # # Create a regular expression  from the dictionary keys
        # multiples = re.findall(r"\$(.*)\$",  text)
        # regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
        # ret = []
        # # For each match, look-up corresponding value in dictionary
        # for text in multiples:
        #     ret.append(regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) )
        #return ret
        for k, v in dict.iteritems():
            text = text.lower().replace(k, v)
        return text




import sys

conv = Converter()
print conv.sub(sys.argv[1])
