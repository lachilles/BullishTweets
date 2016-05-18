from sys import argv
from pprint import pprint
import json, requests
import os   # To access our OS environment variables
# Import the necessary methods from "twitter" library
from twitter import *

# import datetime
# from model import Stock


# Variables that contains the user credentials to access Twitter API 

def get_quotes_by_api(ticker):
    """Return intraday quotes for past 10 days"""
    ##Static url for AAPL##
    #url = 'http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=10d/json'

    # Use below url with row 5 (Stock class)
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
    stock_quote = json.loads(json_string)

    return stock_quote


# def verify_twitter_creds():
#     api = twitter.Api(
#     consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
#     consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
#     access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
#     access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

#     # This will print info about credentials to make sure
#     # they're correct
#     print api.VerifyCredentials()


# def get_tweets_by_api(ticker):
#     """Return latest tweets for past two weeks on a single ticker"""
#     ticker = "$" + ticker
#     tweets = api.GetSearch(term=ticker,count=200)


### reference http://fellowship.hackbrightacademy.com/materials/f14g/lectures/apis/
