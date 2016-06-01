from sys import argv
from pprint import pprint
import json
import requests
import os   # To access our OS environment variables
import twitter  # Import the necessary methods from "twitter" library
from datetime import datetime
import moment
# from model import Stock


# Variables that contains the user credentials to access Twitter API
api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


def get_quotes_by_api(ticker):
    """Return intraday quotes for past 2 days"""
    #return json.dumps([{"date":"2016-05-24 12:58:59","value":260100},{"date":"2016-05-24 12:59:00","value":719300},{"date":"2016-05-24 13:00:00","value":100}])
    #Static url for AAPL##
    # url = 'http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=10d/json'

    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + ticker + '/chartdata;type=quote;range=2d/json'

    #Request data
    r = requests.get(url)

    #Strip extra characters from URL
    header = 'finance_charts_json_callback('
    json_string = r.text[len(header):-1]
    json_string = json_string.strip()

    #Convert JSON to Python dictionary
    stock_quotes = json.loads(json_string)

    clean_stock_quotes, bar = clean_timestamps(stock_quotes)
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


def clean_timestamps(stock_quotes, timespan=24):
    """Transform Epoch timestamp to %Y-%m-%d %H:%M:%S"""

    bar = {
        # "2016-07-16 09:30:00": 250
    }
    num_results = len(stock_quotes["series"])

    # print "&&&&&&&&&&"
    # print "num_results is: " + str(num_results)
    # print "&&&&&&&&&&"

    clean_stock_quotes = []

    for i in range(num_results):
        stock_quote = stock_quotes["series"][i]
        timestamp = stock_quote["Timestamp"]
        clean_timestamp = (datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
        prefix = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:')

        # now = moment.utcnow()
        # if timespan == 1:
        #     moment.utcnow().subtract(hours=1).format("YYYY-MM-DD HH:MM:S")

        # elif timespan == 6:
        #     moment.utcnow().subtract(hours=1).format("YYYY-MM-DD HH:MM:S")

        # elif timespan == 12:

        # elif timespan == 24:


        # If minute is less than 30, take prefix and concatinate minutes
        # which becomes the bar key

        if int(datetime.fromtimestamp(timestamp)
               .strftime('%M')) < 30:
            time = prefix + '00:00'
        else:
            time = prefix + '30:00'

        #Calculates sum of volume in time
        if time in bar:
            bar[time] = bar[time] + stock_quote["volume"]
        else:
            bar[time] = stock_quote["volume"]

        # is time in bar, if not append.
        clean_stock_quote = {"Timestamp": clean_timestamp, "close": stock_quote["close"],
                             "volume": stock_quote["volume"]}
# timestamp, price, volume
# clean_timestamp, close, volume

        clean_stock_quotes.append(clean_stock_quote)

    return clean_stock_quotes, bar


# def get_bar_data(timespan=48):
#     """Gets volume data for timespan up to 48 hours"""
#     bar = {
#         # "2016-07-16 09:30:00": 250
#     }

#     clean_timestamps(stock_quotes)
#     for i in clean_stock_quotes:
#         prefix = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:')
#         # If minute is less than 30, take prefix and concatinate minutes
#         # which becomes the bucket key
#         if int(datetime.datetime.fromtimestamp(timestamp)
#                .strftime('%M')) < 30:
#             timespan = prefix + '00:00'
#         else:
#             timespan = prefix + '30:00'

#         #Calculates sum of volume in timespan
#         if timespan in bar:
#             bar[timespan] = bar[timespan] + clean_stock_quotes["volume"]
#         else:
#             bar[timespan] = clean_stock_quotes["volume"]

#         # is timespan in bar, if not append.
#     return bar


### reference http://fellowship.hackbrightacademy.com/materials/f14g/lectures/apis/
