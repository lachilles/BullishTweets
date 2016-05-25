"""Utility file to that performs functions related to ML"""

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
                values(sentiment='positive')
                db.session.commit
                print Tweet.tweet_id + " has a sentiment of " + Tweet.sentiment
            elif operator == 'neu' or 'neutral':
                stmt = update(tweet).where(tweet.tweet_id==Tweet.tweet_id).\
                values(sentiment='neutral')
                db.session.commit
                print Tweet.tweet_id + " has a sentiment of " + Tweet.sentiment
            elif operator == 'neg' or 'negative':
                stmt = update(tweet).where(tweet.tweet_id==Tweet.tweet_id).\
                values(sentiment='negative')
                db.session.commit
                print Tweet.tweet_id + " has a sentiment of " + Tweet.sentiment
            elif operator == 'q':
                print "goodbye"
                break
            else:
                print "I don't understand that sentiment"

label_tweets()

if __name__ == "__main__":
    connect_to_db(app)
