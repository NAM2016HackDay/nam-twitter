import sys
import tweepy
from zoo_credentials import *
import random
import re
import json
import os.path

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

        self.api.update_status(string[:140])


class Converter():
    """
    Look up the galaxy filename corresponding to a given string
    """

    def __init__(self):
        self.dictionary = {}
        with open('galaxies.txt','r') as r:
            for line in r:
                data = line.split('\t')
                gal_id = int(data[0])
                strings = data[1].split(', ')
                prob = float(data[2])
                for i in strings:
                    if i not in self.dictionary:
                        self.dictionary[i] = [gal_id,prob]
                    else:
                        if self.dictionary[i][1] < prob:
                            self.dictionary[i] = [gal_id,prob]

        pretty_dictionary = {}
        with open('pretty_galaxies.txt','r') as r:
            for line in r:
                data = line.split('\t')
                gal_id = int(data[0])
                strings = data[1].split(', ')
                prob = float(data[2])
                for i in strings:
                        if i not in pretty_dictionary:
                                pretty_dictionary[i] = [gal_id,prob]
                        else:
                                if pretty_dictionary[i][1] < prob:
                                        pretty_dictionary[i] = [gal_id,prob]

        for i in self.dictionary.keys():
                if i in pretty_dictionary.keys():
                        if pretty_dictionary[i][1] > 0.5*self.dictionary[i][1]:
                                self.dictionary[i] = [pretty_dictionary[i][0],pretty_dictionary[i][1]]


    def select_galaxy(self, text):
        text = text.lower()
        if text in self.dictionary:
            success = True
            word = text
            imgid = self.dictionary[word][0]
        else:
            success = False
            word = random.choice(self.dictionary.keys())
            imgid = self.dictionary[word][0]
        return success, '{}.jpg'.format(imgid), word


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
        reply = tweet.get('in_reply_to_status_id')
        from_self = tweet.get('user',{}).get('id_str','') == "747807887658000384" #account_user_id
        #print tweet.get('user',{}).get('id_str','')
        if retweeted is not None and not retweeted and not from_self and not reply:
            tweetText = tweet.get('text')
            if tweetText.lower().startswith('@galaxymenagerie') and not tweetText.startswith('RT'):
                self.process_tweet(tweet)


    def process_tweet(self, tweet):
        tweetText = tweet.get('text')
        tweetId = tweet.get('id_str')
        screenName = tweet.get('user',{}).get('screen_name')

        tweetText = tweetText.replace('@GalaxyMenagerie', '').replace('@galaxymenagerie', '').strip()[:40]
        if len(tweetText) == 0:
            tweetText = "nothing"

        success, img, galaxyText = conv.select_galaxy(tweetText.lower())

        if success:
            replyText = 'This is the galaxy which looks most like a {}'.format(tweetText)
        else:
            replyText = "There's no {}, but here's ".format(tweetText)
            replyText += 'the galaxy which looks most like a {}'.format(galaxyText)

        maxlen = (109 - len(screenName))
        if len(replyText) > maxlen:
            replyText = replyText[0:maxlen] + '...'

        replyText += ' @' + screenName

        #check if response is over 140 char

        #print('Tweet ID: ' + tweetId)
        #print('From: ' + screenName)
        #print('Tweet Text: ' + tweetText)
        #print('Reply Text: ' + replyText)

        filename = os.path.join('galaxies/', img)

        # If rate limited, the status posts should be queued up and sent on an interval
        self.api.update_with_media(filename, status=replyText, in_reply_to_status_id=tweetId)


    def on_error(self, status):
        print status

if __name__ == '__main__':
    twitter = Twitter()
    conv = Converter()
    streamListener = ReplyToTweet(conv)
    twitterStream = Stream(streamListener.auth, streamListener)
    twitterStream.userstream(_with='user')
