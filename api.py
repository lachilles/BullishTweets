from sys import argv
from pprint import pprint
import json, requests

def get_quotes_by_api(ticker):
    """Return intraday quotes for past 10 days"""
    ##Static url for AAPL###
    url='http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=10d/json'
    #Set payload
    #payload = {'key1': 'value1', 'key2': ['value2', 'value3']}

    #Request data
    r = requests.get(url)
    #Convert JSON to Python dictionary
    response_body = r.json()
    
    print response_body

    num_results = response_body['resultCount']

    for i in range(num_results):
        timeStamp = response_body['results'][i].get('Timestamp')
        close = response_body['results'][i].get('close')
        volume = response_body['results'][i].get('volume')
    print "%n :%n :%n" % (timeStamp, close, volume)


get_quotes_by_api('AAPL')

### reference http://fellowship.hackbrightacademy.com/materials/f14g/lectures/apis/
