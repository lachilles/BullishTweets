from sys import argv
from pprint import pprint
import json
import requests
import os   # To access our OS environment variables
import twitter  # Import the necessary methods from "twitter" library
import datetime
# from model import Stock


# Variables that contains the user credentials to access Twitter API
api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


def clean_timestamps(stock_quotes):
    """Transform Epoch timestamp to %Y-%m-%d %H:%M:%S"""

    num_results = len(stock_quotes["series"])


    # print "&&&&&&&&&&"
    # print "num_results is: " + str(num_results)
    # print "&&&&&&&&&&"

    clean_stock_quotes = []

    for i in range(num_results):
        stock_quote = stock_quotes["series"][i]
        timestamp = stock_quote["Timestamp"]
        clean_timestamp = (datetime.datetime.fromtimestamp(timestamp)
            .strftime('%Y-%m-%d %H:%M:%S'))

        clean_stock_quote = {"Timestamp": clean_timestamp, "close": stock_quote["close"],
                             "volume": stock_quote["volume"]}
# timestamp, price, volume
# clean_timestamp, close, volume

        clean_stock_quotes.append(clean_stock_quote)

    return clean_stock_quotes

# 5/16 3pm last error:
# TypeError: 'builtin_function_or_method' object has no attribute '__getitem__'


def get_quotes_by_api(ticker):
    """Return intraday quotes for past 10 days"""
    ##Static url for AAPL##
    #url = 'http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=10d/json'

    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + ticker + '/chartdata;type=quote;range=10d/json'

    #Set payload
    #payload = {'key1': 'value1', 'key2': ['value2', 'value3']}

    #Request data
    r = requests.get(url)

    #Strip extra characters from URL
    header = 'finance_charts_json_callback('
    json_string = r.text[len(header):-1]
    json_string = json_string.strip()

    #Convert JSON to Python dictionary
    stock_quotes = json.loads(json_string)

    clean_stock_quotes = clean_timestamps(stock_quotes)
    print "&&&&&&&&&&&&&&&&&&&&&&&&"
    print clean_stock_quotes
    print "&&&&&&&&&&&&&&&&&&&&&&&&"
    return clean_stock_quotes


def verify_twitter_creds():
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # This will print info about credentials to make sure
    # they're correct
    print api.VerifyCredentials()


def get_tweets_by_api(ticker, n):
    """Return latest tweets for past two weeks on a single ticker"""
    ticker = "$" + ticker
    tweets = api.GetSearch(term=ticker, count=n)

    return tweets




### reference http://fellowship.hackbrightacademy.com/materials/f14g/lectures/apis/
