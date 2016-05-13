from sys import argv
from pprint import pprint
import json

import requests

def get_quotes_by_api(ticker):
    """Return intraday quotes for past 10 days"""

    url='http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=1d/json'
    response = requests.get(url)
    response_body = response.json()
    

    return 

def get_json():
    """Converts interval_data to JSON"""
    stock_json = interval_data.json()

    num_results = stock_json['resultCount']

    for i in range(num_results):
