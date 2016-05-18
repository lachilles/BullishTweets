"""Stocks"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Stock, connect_to_db, db
# need to import Tweet table as part of phase 2


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/stock-detail")
def stock_detail():
    """Show stock details"""
    ticker = request.args.get("ticker")
    current_stock = Stock.query.get(ticker)
    # spx_member = Stock.query.filter_by(ticker="ticker").first()

    # #Provide feedback to user on whether if ticker is valid
    # if not spx_member:
    #     flash("Please enter a valid ticker symbol")

    quotes = current_stock.get_quotes()
    tweets = current_stock.get_tweets()

    #num_results = len(quotes["series"])

    # for i in range["num_results"]:
    #     (datetime.datetime.fromtimestamp(
    #         int(quotes["series"][i]["Timestamp"])
    #         ).strftime('%Y-%m-%d %H:%M:%S'))
    #     return quotes["series"][i]["Timestamp"]
    #5/16 3pm last error:
    #TypeError: 'builtin_function_or_method' object has no attribute '__getitem__'

    return render_template("stock-detail.html",
                           stock=current_stock,
                           quotes=quotes, tweets=tweets)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
