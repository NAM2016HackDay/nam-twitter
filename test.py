import tweepy
import arxiv
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)




s = "GW150914"

results = arxiv.query(s, prune=True, start=0, max_results=10)

for result in results:
    api.update_status(result['title'][:140])
    print result['title'][:140]



