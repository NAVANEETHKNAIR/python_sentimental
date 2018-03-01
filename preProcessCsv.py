import csv
import sys
import re
from nltk.corpus import stopwords
import nltk.classify

stop_words = set(stopwords.words("english"))
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

def processTweets(tweet):
    feature_vector=[]
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
    # return the filtered list
    return tweet


featureList = []
tweets = []
stop_words = set(stopwords.words("english"))
f = open(sys.argv[1], 'rt')
target = open("result.txt", "w")

#getting the feature vector by eliminating the stop words and punctuations
def getFeatureVector(tweet):
    feature_vector=[]
    words=tweet.split()
    for word in words:
        if word not in stop_words:
            feature_vector.append(word.lower().strip('\'"?,.\\'))
    return feature_vector

try:
    reader = csv.reader(f)
    next(reader, None)  # skip the header
    for row in reader:
        if row[1] == "1":
            sentiment = "positive"
        else:
            sentiment = "negative"
        #cleaning the tweet removing url's,username,hashtags
        processed_tweets=processTweets(row[3])
        #building the feature vector
        featureVector=getFeatureVector(processed_tweets)
        #building the feature list
        featureList.extend(featureVector)
        tweets.append((featureVector, sentiment))
finally:
    f.close()
    target.close()
featureList = list(set(featureList))
#here we are passing the tweets variable to the extract_features function
training_set = nltk.classify.util.apply_features(extract_features, tweets)
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

testTweet = 'I do not like this car'
processedTestTweet = processTweets(testTweet)
print NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
#training_set = nltk.classify.util.apply_features(extract_features, tweets)
# Remove featureList duplicates
#target.write(sentiment + "," + " ".join(processTweets(row[3])))
#target.write("\n")
