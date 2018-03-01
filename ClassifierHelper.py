__author__ = 'hharwani'
import re
import nltk
from nltk.classify import *

class ClassifierHelper:
    #start __init__
    def __init__(self, featureListFile):
        self.wordFeatures = []
        # Read feature list
        inpfile = open(featureListFile, 'r')
        line = inpfile.readline()
        while line:
            self.wordFeatures.append(line.strip())
            line = inpfile.readline()
    #end

    #start extract_features
    def extract_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.wordFeatures:
            word = self.replaceTwoOrMore(word)
            word = word.strip('\'"?,.')
            features['contains(%s)' % word] = (word in document_words)
        return features
    #end

    #start replaceTwoOrMore
    def replaceTwoOrMore(self, s):
        # pattern to look for three or more repetitions of any character, including
        # newlines.
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)
    #end

    #start process_tweet
    def process_tweet(self, tweet):
         tweet = tweet.lower()
    # removing the url's and any web address
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet)
    # removing usernames followed by @
    tweet = re.sub('@[^\s]+', '', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = re.sub('(?<=\w)\.(?=\w+\.)|\G\w+\)', '', tweet)
    # removing extra dotes
    tweet = re.sub('[\d\.]', "", tweet)
    # removing special characters like !,<,>,|,@
    tweet = re.sub('[!-><|@]', "", tweet)
    # tokenze the tweets
    tweet=tweet.strip('\'"?,.')
    # remove the stop words and punctuations
    #end

    #start is_ascii
    def is_ascii(self, word):
        return all(ord(c) < 128 for c in word)
    #end
#end class