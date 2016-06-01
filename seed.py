"""Utility file to seed stock data from S&P 500 constituents in seed_data/"""

from sqlalchemy import func
from model import Stock, Tweet
from model import connect_to_db, db
from server import app
from api import get_tweets_by_api
import unicodedata

# import datetime


def load_stocks():
    """Load stocks from SPX_constituents into database."""

    print "Stocks"

    # count = 1
    # Read u.user file and insert data
    for row in open("seed_data/SPX_constituents-tab.txt", "U"):
        # row = row.strip()
        ticker, name, sector, industry = row.split("\t")
        print row
        stock = Stock(ticker=ticker,
                      name=name,
                      sector=sector,
                      industry=industry)

        # We need to add to the session or it won't ever be stored
        db.session.add(stock)
        # print "added" + stock
        # print count
        # count += 1

    # Once we're done, we should commit our work
    db.session.commit()


def load_tweets_from_txt():
    """Load tweets from txt file into database."""

    print "Tweets from txt"

    count = 1
    for row in open("seed_data/tweet-training-sets-import-tab.txt", "U"):
        row = row.strip()
        token = row.split("\t")
        print token
        print len(token)
        if len(token) >= 10:

            tweet_id = token[0]
            ticker = token[1]
            date_time = token[2]
            text = token[3]
            user = token[4]
            retweet_count = token[5]
            sentnum_tr = token[6]
            sentiment_tr = token[7]
            sentnum_nltk = token[8]
            sentiment_nltk = token[9]

            tweet = Tweet(tweet_id=tweet_id,
                          ticker=ticker,
                          date_time=date_time,
                          text=text,
                          user=user,
                          retweet_count=retweet_count,
                          sentnum_tr=sentnum_tr,
                          sentiment_tr=sentiment_tr,
                          sentnum_nltk=sentnum_nltk,
                          sentiment_nltk=sentiment_nltk
                          )

            db.session.add(tweet)
            print "added" + str(tweet)
            print count
            count += 1

    db.session.commit()


def is_good_tweet(tweet):
    """Ignore tweets with more than 1 $ symbol and ignore retweets"""

    return tweet.text.count('$') == 1 and tweet.retweeted_status is None


def load_tweets(count, since_id):
    """Return n tweets for a list of tickers"""

    #For 10 sample tickers, retrieve n tweets each
    # tech_tickers = ['AAPL', 'FB', 'MSFT', 'GOOGL', 'HPQ', 'V', 'INTC', 'CSCO', 'IBM', 'ORCL']

    #Fetch all Stocks
    stocks = Stock.query.all()

    #Iterate through Stocks and append ticker to list

    SPX_constituents = []

    for stock in stocks:
        ticker = unicodedata.normalize('NFKD', stock.ticker).encode('ascii', 'ignore')
        SPX_constituents.append(ticker)

    bad_tweets = 0

    #Set payload for getting tweets
    # if payload is None:
    #     payload = {'count': n}

    #Identify unique tweets in this set
    unique_tweet_ids = set()

    for ticker in SPX_constituents[301:400]:
        tweets = get_tweets_by_api(term=ticker, count=count, since_id=since_id)

        #parse the tweets for this ticker
        counter = 0
        for tweet in tweets:
            if not is_good_tweet(tweet):
                bad_tweets += 1
                # continue
                #create tweet object
            else:
                if tweet.id not in unique_tweet_ids:
                    t = Tweet(
                        tweet_id=tweet.id,
                        tweet_id_str=tweet.id_str,
                        ticker=ticker,
                        date_time=tweet.created_at,
                        text=tweet.text,
                        user=tweet.user.screen_name,
                        retweet_count=tweet.retweet_count
                        )

                    db.session.add(t)
                    counter += 1
                    unique_tweet_ids.add(tweet.id)

        good_tweets = str(counter)
        print "Found " + good_tweets + " good tweets for " + ticker

    print "Found " + str(bad_tweets) + " total bad tweets out of " + str(count * len(SPX_constituents))

    db.session.commit()


def load_new_tweets(count):
    """Append n tweets to DB since initial load"""

    since_id = db.session.query(func.max(Tweet.tweet_id)).first()
    since_id = int(since_id[0])

    load_tweets(count=count, since_id=since_id)


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Delete tweets and stocks
    # Tweet.query.delete()
    # Stock.query.delete()

    # Import different types of data
    # load_stocks()

    # load_tweets(500, None)

    load_new_tweets(count=500)

    # load_tweets_from_txt()
