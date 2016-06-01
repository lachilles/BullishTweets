"""Stocks"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
from sqlalchemy import func
from model import Stock, Tweet, connect_to_db, db
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
def stock_detail_from_link(ticker):
    """Show stock details from links"""
    current_stock = Stock.query.get(ticker)

    quotes, bar = current_stock.get_quotes()
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
    print "****************************"
    print timespan
    print "****************************"

    # datetime = quotes.Timestamp
    # volume = quotes.volume

    result = []

    for key, value in bar.iteritems():
        result.append({'date': key, 'value': value})
        # print "The timestamp should be: " + bar[key: value]
    return json.dumps(result)


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
