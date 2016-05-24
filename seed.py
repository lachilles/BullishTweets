"""Utility file to seed stock data from S&P 500 constituents in seed_data/"""

from sqlalchemy import func
from model import Stock, Tweet
# from model import Stock

from model import connect_to_db, db
from server import app
from api import get_tweets_by_api

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


def is_good_tweet(tweet):
    """Ignore tweets with more than 1 $ symbol and ignore retweets"""

    return tweet.text.count('$') == 1 and tweet.retweeted_status is None


def load_tweets(n):
    """Return n tweets for a list of tickers"""

    #For 10 sample tickers, retrieve n tweets each
    tech_tickers = ['AAPL', 'FB', 'MSFT', 'GOOGL', 'HPQ', 'V', 'INTC', 'CSCO', 'IBM', 'ORCL']
    bad_tweets = 0
    #Identify unique tweets in this set
    unique_tweet_ids = set()

    for ticker in tech_tickers:
        tweets = get_tweets_by_api(ticker, n)

        #parse the tweets for this ticker
        count = 0
        for tweet in tweets:
            if not is_good_tweet(tweet):
                bad_tweets += 1
                # continue
                #create tweet object
            else:
                if tweet.id not in unique_tweet_ids:
                    t = Tweet(
                        tweet_id=tweet.id,
                        ticker=ticker,
                        date_time=tweet.created_at,
                        text=tweet.text,
                        user=tweet.user.screen_name,
                        retweet_count=tweet.retweet_count)

                    db.session.add(t)
                    count += 1
                    unique_tweet_ids.add(tweet.id)

        print "Found " + str(count) + " good tweets for " + ticker

    print "Found " + str(bad_tweets) + " total bad tweets out of " + str(n * len(tech_tickers))

    db.session.commit()

# def load_new_tweets(n):
#     """Append n tweets to DB since initial load"""

#     session.query(func.max(tweet.tweet_id))


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Delete tweets and stocks
    # Tweet.query.delete()
    Stock.query.delete()
    # Import different types of data
    load_stocks()

    load_tweets(100)
