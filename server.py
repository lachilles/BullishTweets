"""Stocks"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
from sqlalchemy import func
from model import Stock, Tweet, connect_to_db, db
import unicodedata
import moment
from datetime import datetime
import time
import random
from sentiment import Sentiment
# need to import Tweet table as part of phase 2

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage showing list of SPX members"""
    stocks = Stock.query.all()

    return render_template("homepage.html", stocks=stocks)


@app.route("/stock-detail")
def stock_detail():
    """Show stock details on form submit"""
    ticker = request.args.get("ticker").upper()
    session['ticker'] = ticker
    print "In our session is " + session['ticker']
    current_stock = Stock.query.get(ticker)
    # spx_member = Stock.query.filter_by(ticker="ticker").first()

    #Provide feedback to user on whether if ticker is valid

    if current_stock is None:
        flash("Please enter a valid ticker symbol")
        return render_template("homepage.html")

    quotes, bar = current_stock.get_quotes('24')
    tweets = current_stock.get_tweets()

    return render_template("stock-detail.html",
                           stock=current_stock,
                           quotes=quotes, tweets=tweets)


@app.route("/stock-detail/<ticker>")
def stock_detail_from_link(ticker, timespan=24):
    """Show stock details from links"""
    current_stock = Stock.query.get(ticker)

    quotes, bar = current_stock.get_quotes(timespan)
    tweets = current_stock.get_tweets()

    return render_template("stock-detail.html",
                           stock=current_stock,
                           quotes=quotes, tweets=tweets)


@app.route("/data.json/<timespan>")
def get_bar_data(timespan):
    """Send stock volume data to bar chart"""
    print "In our JSON route" + session.get("ticker")
    ticker = session.get("ticker")
    # ticker = request.args.get("stock.ticker")

    current_stock = Stock.query.get(ticker)
    quotes, bar = current_stock.get_quotes(timespan)
    # print "****************************"
    # print timespan
    # print "****************************"

    # datetime = quotes.Timestamp
    # volume = quotes.volume

    result = []

    for key, value in bar.iteritems():
        result.append({'date': key, 'value': value})
        # print "The timestamp should be: " + bar[key: value]
    return json.dumps(result)

# can only have one route returning a json of: {bar chart data{},sentiment_data{}}?


@app.route("/scatterdata.json/<timespan>")
def get_scatter_data(timespan):
    """Send tweet sentiment to scatter plot"""
    print "In our JSON route" + session.get("ticker")
    ticker = session.get("ticker")
    current_stock = Stock.query.get(ticker)
    tweets = current_stock.get_tweets()
    stocks = Stock.query.all()

    # tweets_json = json.dumps(tweets, default=lambda o: o.__dict__)

    # now = moment.utcnow().timezone("US/Eastern")
    result = []
    s = Sentiment(stocks)
    sentiment = None
    negative = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5']
    positive = ['0.6', '0.7', '0.8', '0.9', '1.0']

    for tweet in tweets:
        tweet_text = unicodedata.normalize('NFKD', tweet.text).encode('ascii', 'ignore')
        # Get the sentiment of the tweet retured in either 'positive' or 'negative'
        sentiment_str = s.get_tweet_sentiment(tweet_text)
        if sentiment_str == 'positive':
            sentiment = random.choice(positive)
        if sentiment_str == 'negative':
            sentiment = random.choice(negative)
        created_at = unicodedata.normalize('NFKD', tweet.created_at).encode('ascii', 'ignore')
        # Sun Jun 05 17:09:07 +0000 2016
        created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))
        print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        print created_at
        print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        result.append({'datetime': created_at, 'sentiment': sentiment})
    return json.dumps(result)



    # tweets_w_sentiment = Tweet.query.filter(Tweet.sentiment is None).limit(5000).all()
    # unicodedata.normalize('NFKD', tweet.text).encode('ascii', 'ignore')
    #     tweets.append(tweet)

    #     bar = {
    #     # "2016-07-16 09:30:00": 250
    # }
    # num_results = len(stock_quotes["series"])

    # # print "&&&&&&&&&&"
    # # print "num_results is: " + str(num_results)
    # # print "&&&&&&&&&&"

    # print "&&&&&&&&&& TIMESPAN IS: &&&&&&&&&&"
    # print timespan == '12'
    # print timespan
    # print "&&&&&&&&&&"

    # clean_stock_quotes = []

    # for i in range(num_results):
    #     stock_quote = stock_quotes["series"][i]
    #     unix_timestamp = stock_quote["Timestamp"]


    # for tweet in tweets:
    #     tweet = get_tweet_sentiment(tweet)
    #     db.session.add(tweet)
    #     db.commit()

# @app.route("/sentiment")
# def sentiment(ticker):
#     """Container for sentiment area chart"""

#     tweets_w_sentiment = Tweet.query.filter(Tweet.sentiment is not None).limit(5000).all()

#     return render_template("sentiment.html", tweets_w_sentiment=tweets_w_sentiment)


# @app.route("/admin")
# def label_tweets(ticker):
#     """Administrative function to label sentiment on tweets manually"""

#     tweets_wo_sentiment = Tweet.query.filter(Tweet.sentiment is None).limit(5000).all()

#     return render_template("admin.html", tweets_wo_sentiment=tweets_wo_sentiment)

# @app.route("/spx-member")
# def is_spx_member():
#     """Provide feedback to user on whether if ticker is valid"""

if __name__ == "__main__":
# We have to set debug=True here, since it has to be True at the point
# that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbars
    DebugToolbarExtension(app)

    app.run()
