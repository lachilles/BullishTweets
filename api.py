from sys import argv
from pprint import pprint
import json
import requests
import os   # To access our OS environment variables
import twitter  # Import the necessary methods from "twitter" library
from datetime import datetime
import moment
# from tokenizer import Tokenizer
# from model import Tweet, connect_to_db, db
# from server import app
# Moment documentation: https://github.com/zachwill/moment


# Variables that contains the user credentials to access Twitter API
api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


def get_quotes_by_api(ticker, timespan):
    """Return intraday quotes for past day"""
    #return json.dumps([{"date":"2016-05-24 12:58:59","value":260100},{"date":"2016-05-24 12:59:00","value":719300},{"date":"2016-05-24 13:00:00","value":100}])
    #Static url for AAPL##
    # url = 'http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=10d/json'

    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + ticker + '/chartdata;type=quote;range=1d/json'

    #Request data
    r = requests.get(url)

    #Strip extra characters from URL
    header = 'finance_charts_json_callback('
    json_string = r.text[len(header):-1]
    json_string = json_string.strip()

    #Convert JSON to Python dictionary
    stock_quotes = json.loads(json_string)

    clean_stock_quotes, bar = clean_timestamps(stock_quotes, timespan)
    print "&&&&&&&&&&&&&&&&&&&&&&&&"
    print clean_stock_quotes
    print "&&&&&&&&&&&&&&&&&&&&&&&&"
    return clean_stock_quotes, bar


def verify_twitter_creds():
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # This will print info about credentials to make sure
    # they're correct
    print api.VerifyCredentials()


def get_tweets_by_api(term='AAPL', count=200, since_id=None):
    """Return 200 of the most popular tweets on a single ticker"""

    ticker = "$" + term
    #Request data
    tweets = api.GetSearch(term=ticker, count=count, lang='en', since_id=since_id)

    return tweets

# def get_tweets_since_timespan():
#     """Convert """


def clean_timestamps(stock_quotes, timespan):
    """Transform Epoch timestamp to %Y-%m-%d %H:%M:%S"""

    bar = {
        # "2016-07-16 09:30:00": 250
    }
    num_results = len(stock_quotes["series"])

    # print "&&&&&&&&&&"
    # print "num_results is: " + str(num_results)
    # print "&&&&&&&&&&"

    print "&&&&&&&&&& TIMESPAN IS: &&&&&&&&&&"
    print timespan == '12'
    print timespan
    print "&&&&&&&&&&"

    clean_stock_quotes = []

    for i in range(num_results):
        stock_quote = stock_quotes["series"][i]
        unix_timestamp = stock_quote["Timestamp"]

        # Create moment from unix_timestamp, convert to EST timezone, and format
        clean_timestamp = moment.unix(unix_timestamp, utc=True).timezone("US/Eastern").format("YYYY-MM-DD HH:MM:ss")
        prefix = moment.unix(unix_timestamp, utc=True).timezone("US/Eastern").strftime('%Y-%m-%d %H:')

        now = moment.utcnow().timezone("US/Eastern")
        if timespan == '1':
            clean_timestamp = now.subtract(hours=1).format("YYYY-MM-DD HH:MM:ss")
            bar[clean_timestamp] = stock_quote["volume"]

        elif timespan == '6':
            clean_timestamp = now.subtract(hours=6).format("YYYY-MM-DD HH:MM:ss")
            bar[clean_timestamp] = stock_quote["volume"]

        elif timespan == '12':
            clean_timestamp = now.subtract(hours=12).format("YYYY-MM-DD HH:MM:ss")
            bar[clean_timestamp] = stock_quote["volume"]

        elif timespan == '24':
            clean_timestamp = now.subtract(hours=24).format("YYYY-MM-DD HH:MM:ss")

            # If minute is less than 30, take prefix and concatinate minutes
            # which becomes the bar key

            if int(moment.unix(unix_timestamp, utc=True).timezone("US/Eastern").strftime('%M')) < 30:
                unix_timestamp = prefix + '00:00'
            else:
                unix_timestamp = prefix + '30:00'

            #Calculates sum of volume in time
            if unix_timestamp in bar:
                bar[unix_timestamp] = bar[unix_timestamp] + stock_quote["volume"]
            else:
                bar[unix_timestamp] = stock_quote["volume"]

        # is time in bar, if not append.
        clean_stock_quote = {"Timestamp": clean_timestamp, "close": stock_quote["close"],
                             "volume": stock_quote["volume"]}
# timestamp, price, volume
# clean_timestamp, close, volume

        clean_stock_quotes.append(clean_stock_quote)

    return clean_stock_quotes, bar


# def get_sentiment_by_api():
#         """Gets tweet sentiment from sentiment140"""
#         tweets_wo_sentiment = Tweet.query.filter(Tweet.sentiment is None).limit(5000).all()
#         url = 'http://www.sentiment140.com/api/bulkClassifyJson'

#         tweets = []

#         for tweet in tweets_wo_sentiment:
#                 tweets.append({"text": Tweet.text, "query": Tweet.ticker})

#         info = {"data": tweets}
#         data = json.dumps(info)

#             #Request data
#         r = requests.post(url, data)
#         results = r.json()

#         index = 0

#         for result in results['data']:
#             polarity = int(result['polarity'])

#             if polarity == 4:
#                 sentiment = 'positive'
#             elif polarity == 0:
#                 sentiment = 'negative'
#             else:
#                 sentiment = 'neutral'

#             tweets_wo_sentiment[index].sentiment = sentiment
#             index += 1

#         db.session.commit()

#         print "Tweet sentiments updated."



# def round_to_nearest(num, base):
#     """Function to round to nearest 30 minutes"""
#     n = num + (base//2)

#     return n - (n % base)

### reference http://fellowship.hackbrightacademy.com/materials/f14g/lectures/apis/
