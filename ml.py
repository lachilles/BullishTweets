"""Utility file that performs functions related to ML"""
#Source: http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
# https://indico.io/blog/plotlines/

from sqlalchemy import func, update
from model import Stock, Tweet
# from model import Stock

from model import connect_to_db, db
from server import app
from api import get_tweets_by_api


def label_tweets():
    """Simple program that let's you label tweets sentiment from the console"""
    tweets_wo_labels = db.query(Tweet).filter(Tweet.sentiment=None).all()

    repeat = 1
    while repeat > 0:
        for tweet in tweets_wo_labels:
            print Tweet.tweet_id
            print Tweet.text
            user_input = raw_input("Please provide sentiment>>")
            user_input = user_input.strip()
            tokens = user_input.split(" ")
            for item in tokens:
                if item == '':
                    tokens.remove('')
                else:
                    pass

            operator = tokens[0]

            if operator == 'p' or 'pos' or 'positive':
                stmt = update(tweet).where(tweet.tweet_id==Tweet.tweet_id).\
                values(sentnum_tr='positive')
                db.session.commit
                print Tweet.tweet_id + " has a sentiment of " + Tweet.sentiment
            elif operator == 'neu' or 'neutral':
                stmt = update(tweet).where(tweet.tweet_id==Tweet.tweet_id).\
                values(sentnum_tr=0)
                db.session.commit
                print Tweet.tweet_id + " has a sentiment of " + Tweet.sentiment
            elif operator == 'neg' or 'negative':
                stmt = update(tweet).where(tweet.tweet_id==Tweet.tweet_id).\
                values(sentnum_tr= -1)
                db.session.commit
                print Tweet.tweet_id + " has a sentiment of " + Tweet.sentiment
            elif operator == 'q':
                print "goodbye"
                break
            else:
                print "I don't understand that sentiment"

label_tweets()

def create_training_set():
    """Function to prepare a training set of tweets with labels"""

    # Split training set into pos_tweets, neg_tweets list
    pos_tweets = []
    neg_tweets = []
    tweets_w_labels = Tweet.query.filter_by(sentnum_tr != None).all()

    for tweet in tweets:
        if tweet.sentnum_tr == 0:
            pass
        elif tweet.sentnum_tr == 1:
            pos_tweets += (str(tweet.text), 'positive')
        elif tweet.sentnum_tr == -1:
            neg_tweets += (str(tweet.text), 'negative')

    #Take both lists and create a single list of tuples
    tweets = []

    for (words, sentiment) in pos_tweets + neg_tweets:
        words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
        tweets.append((words_filtered, sentiment))

    print "Tweets list: " + tweets

    
    #Combined list with the training set of tweets









if __name__ == "__main__":
    connect_to_db(app)
