# BullishTweets

BullishTweets allow users to search for any stock in the S&P 500 Index, and look at the most recent intraday trading activity, side by side with the most recent tweets on that stock. It performs sentiment analysis on the most recent tweets and allows the user to visualize bearish/bullish market trends as depicted by social media. 

### Tech Stack
* Languages: Python, Javascript, HTML5, CSS3, PosgreSQL
* Frameworks/Libraries: Flask, D3, SQL Alchemy, jQuery, AJAX, Jinja, Bootrap, NLTK, Regex, Moment
* APIs: Yahoo Finance, Twitter
* Dependencies: Available in requirements.txt

### Features
##### Tweet Sentiment
The sentiment analyzer uses a Naive Bayes classifier from Python's Natural Language Toolkit. The classifier was trained using a hand labeled set of 400 tweets. The scatter plot below is a D3 graph that visualizes sentiment over time.

![scatter](https://github.com/lachilles/HBProject/blob/master/static/images/scatter.png)

##### D3 Graph and Datetime Series
BullishTweets provides granularity of intraday trading activity beyond the minimum timespan of 24 hours that Yahoo Finance provides. The user can click on the 1, 6, 12, 24hr incremented timespan buttons to effectively slice and dice the most recent intraday trading activity for a given stock. 

![bar](https://github.com/lachilles/HBProject/blob/master/static/images/bar.png)

![raw](https://github.com/lachilles/HBProject/blob/master/static/images/raw.png)

I'm using D3's custom directives and asynchronous AJAX calls when the user clicks on a timespan. The 24 hour span includes some clever bucketing logic to agregate all trades into 30 minute increments. The date/time labels are transalated from UTC (from Twitter) and Epoch time (from Yahoo) with Python's datetime string formatting and Moment library. Once the data is back from the server, I'm emptying the existing data and updating the new data into D3 in the callback function.

##### Ticker Search
The landing page and stock details page includes a search form that allows users to search for any ticker symbol in the S&P500

![landing](https://github.com/lachilles/HBProject/blob/master/static/images/landing.png)


