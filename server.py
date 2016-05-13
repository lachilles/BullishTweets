"""Stocks"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

import requests
from model import Stock, connect_to_db, db
# need to import Tweet table as part of phase 2


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

#Matches solution
@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/stock-detail/<ticker>")
def stock_detail(ticker):
    """Show stock details"""
    current_stock = Stock.query.get('AAPL')
    quotes = current_stock.get_quotes()

    # url='http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=1d/csv'
    # response = requests.get(url)
    # response_body = response.content
    # data = response_body.split('\n')
    # # Timestamp, close, high, low, open, volume in data[11]
    # summary = data[12:17]
    # interval_data = data[17:]

    return render_template("stock-detail.html", current_stock=stock, quotes=quotes)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
