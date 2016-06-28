import tweepy
import arxiv
from credentials import *


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

#for result in results:
#   #
#  print result['title'][:140]



