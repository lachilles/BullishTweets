"""
Perform Sentiment Analysis on Tweets using NLTK

Use NLTK on tweet text to target words related to a stock with 'cashtags'
($) preceding the ticker symbol and assess sentiment. Generates a sentiment
score for the tweet based on a probability from 0.0 to 1.0,
where 1.0 is good and 0.0 is bad.

"""
#Source: http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
# https://indico.io/blog/plotlines/

# from sqlalchemy import func, update
from model import Stock
from model import Tweet
import unicodedata
from model import db, connect_to_db
from server import app
import re
import nltk


# ******** PREPROCESSING ********
def processTweet(tweet):
    """Clean tweets"""
    #Fetch all Stocks
    stocks = Stock.query.all()

    #Iterate through Stocks and append ticker and company name to list

    SPX_constituents = []
    company_names = []
    for stock in stocks:
        ticker = unicodedata.normalize('NFKD', stock.ticker).encode('ascii', 'ignore')
        SPX_constituents.append(ticker)
        company_name = unicodedata.normalize('NFKD', stock.name).encode('ascii', 'ignore')
        company_names.append(company_name)

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #Replace $word with word
    tweet = re.sub(r'$([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    #Remove ticker
    big_regex = re.compile('|'.join(map(re.escape, SPX_constituents)))
    tweet = big_regex.sub('', str(tweet))
    #Remove company name
    big_regex = re.compile('|'.join(map(re.escape, company_names)))
    tweet = big_regex.sub('', str(tweet))
    return tweet

#Read the tweets one by one and process it
# fp = open("seed_data/tweet-training-sets-list.txt", "U")
# line = fp.readline()

# print "********Cleaned Tweets********"

# while line:
#     processedTweet = processTweet(text)
#     print processedTweet
#     line = fp.readline()
# #end loop
# fp.close()

# print "********End of Cleaned Tweets********"

# ******** TOKENIZATION *********


def tokenize_tweets():
    """Split training set into pos_tweets, neg_tweets list"""
    # print "Manually labelled training set"

    tweets = []
    pos_tweets = []
    neg_tweets = []
    neu_tweets = []
    count = 0
    for row in open("seed_data/tweet-training-sets-list.txt", "U"):
        row = row.strip()
        token = row.split("\t")
        # print row
        # print len(token)

        text = token[1]
        sentiment_str = token[3]
        processed_tweet = processTweet(text)

        if sentiment_str == 'positive':
            r = (processed_tweet, sentiment_str)
            pos_tweets.append(r)
        elif sentiment_str == 'neutral':
            r = (processed_tweet, sentiment_str)
            neu_tweets.append(r)
        elif sentiment_str == 'negative':
            r = (processed_tweet, sentiment_str)
            neg_tweets.append(r)
        count += 1

    # print "Total rows processed" + str(count)
    # print "**Positive and Negative Tweets**"

    for (words, sentiment) in pos_tweets + neg_tweets:
        words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
        tweets.append((words_filtered, sentiment))

    #Combined list with the training set of tweets
    # print "Tokenized tweets list: "
    return tweets

# # Test set to assess the exactitude of the trained classifier.
# test_tweets = [
#     (['feel', 'happy', 'this', 'morning'], 'positive'),
#     (['larry', 'friend'], 'positive'),
#     (['not', 'like', 'that', 'man'], 'negative'),
#     (['house', 'not', 'great'], 'negative'),
#     (['your', 'song', 'annoying'], 'negative')]

# print '**************FEATURE EXTRACTION***************'

# # The list of word features need to be extracted from the tweets. It is a list
# # with every distinct words ordered by frequency of appearance. We use the
# # following function to get the list plus the two helper functions.


# def features():
#     tweets = tokenize_tweets()
#     word_features = get_word_features(get_words_in_tweets(tweets))
#     return word_features


# Helper functions
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    # word_features = [i[0] for i in wordlist.most_common()]
    return word_features

# print "&&&&&&&&&&&&&&&&&&&&&&&&&&"
# print "Frequency Distribution of Tweets"
# print "&&&&&&&&&&&&&&&&&&&&&&&&&&"


# def get_FreqDist():
#     """NLTK built-in method to view FreqDist"""
#     tweets = tokenize_tweets()
#     FreqDist = nltk.FreqDist(get_words_in_tweets(tweets))
#     return FreqDist


# def get_wf():
#     tweets = tokenize_tweets()
#     word_features = get_word_features(get_words_in_tweets(tweets))
#     return word_features

# print "&&&&&&&&&&&&&&&&&&&&&&&&&&"
# print "Word Features"
# print "&&&&&&&&&&&&&&&&&&&&&&&&&&"


def extract_features(document):
    document_words = set(document)
    features = {}
    # word_features = features()
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


"""Apply features to training_set and train classifier"""


def get_tweet_sentiment(tweet):
    """The Naive Bayes classifier uses the prior probability of each label which
    is the frequency of each label in the training set, and the contribution
    from each feature."""

    # tweet = 'Samsung reaches new highs'
    sentiment = classifier.classify(extract_features(tweet.split()))
    return sentiment

if __name__ == "__main__":
    connect_to_db(app)
    tweets = tokenize_tweets()
    word_features = get_word_features(get_words_in_tweets(tweets))
    training_set = nltk.classify.apply_features(extract_features, tweets)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
