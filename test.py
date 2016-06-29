import sys
import tweepy
#import arxiv
from credentials import *
import re
import json
from collections import OrderedDict
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


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

    def sub(self, string):
        return self.multiple_replace(self.astro_replace, string)

    def parse_dictionary(self, file):
        # TODO: allow multiple, randomly-chosen substitutions
        myvars = OrderedDict()  # ensure substitutions occur in order
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




class ReplyToTweet(StreamListener):

    def __init__(self, conv):
        """
        Authenticates the Python script against the Twitter auth API, and
        sets up the object.
        """
        self.conv = conv
        auth = self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)


    def on_data(self, data):
        if data is not None:
            try:
                self.process_data(data)
            except: # catch *all* exceptions
                print(sys.exc_info()[0])

    def process_data(self, data):
        #print data
        tweet = json.loads(data.strip())

        retweeted = tweet.get('retweeted')
        reply = tweet.get('in_reply_to_user_id')
        #print tweet
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id
        #print tweet.get('user',{}).get('id_str','')
        if retweeted is not None and not retweeted and not from_self and not reply:
            tweetText = tweet.get('text')
            if tweetText.lower().startswith('@nambot2016') and not tweetText.startswith('RT'):
                self.process_tweet(tweet)

    def process_tweet(self, tweet):
        tweetText = tweet.get('text')
        tweetId = tweet.get('id_str')
        screenName = tweet.get('user',{}).get('screen_name')
        tweetText = tweetText.replace("@nambot2016","").replace("@NAMbot2016","")
        tweetText = tweetText.replace("@NAMBOT2016","")
        chatResponse = conv.sub(tweetText) #chatbot.respond(tweetText)
        if tweetText.lower() == chatResponse.lower():
            chatResponse = "@{} That looks pretty good already!".format(screenName)
            replyText =  chatResponse
        else:
            replyText =  chatResponse + ' @' + screenName

        #check if repsonse is over 140 char
        if len(replyText) > 140:
            replyText = replyText[0:137] + '...'

        print('Tweet ID: ' + tweetId)
        print('From: ' + screenName)
        print('Tweet Text: ' + tweetText)
        print('Reply Text: ' + replyText)

        # If rate limited, the status posts should be queued up and sent on an interval
        self.api.update_status(status=replyText, in_reply_to_status_id=tweetId)

    def on_error(self, status):
        print status

if __name__ == '__main__':
    twitter = Twitter()
    conv = Converter()
    streamListener = ReplyToTweet(conv)
    twitterStream = Stream(streamListener.auth, streamListener)
    twitterStream.userstream(_with='user')
