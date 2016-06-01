"""Models and database functions for Stock Sentiment project."""


from flask_sqlalchemy import SQLAlchemy
from api import get_quotes_by_api, get_tweets_by_api

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions


class Stock(db.Model):
    """Stocks in S&P500"""

    __tablename__ = "stocks"

    ticker = db.Column(db.String(6), nullable=False, primary_key=True)
    name = db.Column(db.String(42), nullable=False)
    sector = db.Column(db.String(30), nullable=False)
    industry = db.Column(db.String(56), nullable=False)
    correlation = db.Column(db.Numeric)

    tweets = db.relationship('Tweet')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "Stock ticker=%s name=%s>" % (self.ticker, self.name)

    def get_quotes(self):
        """Return intraday quotes for past 10 days"""
        return get_quotes_by_api(self.ticker)

    def get_tweets(self):
        """Return last tweets on ticker"""
        return get_tweets_by_api(self.ticker)

    # def save_object(self, filename):
    #     """Save python object"""
    #     with open(filename,)

#     # url='http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=1d/csv'
    # response = requests.get(url)
    # response_body = response.content
    # data = response_body.split('\n')
    # # Timestamp, close, high, low, open, volume in data[11]
    # summary = data[12:17]
    # interval_data = data[17:]

    # def price_str(self):
    #     """Return price formatted as string $x.xx"""

    #     return "$%.2f" % self.price

class Tweet(db.Model):
    """Tweets on stocks"""

    ___tablename__ = "tweets"

    tweet_id = db.Column(db.String(64), nullable=False, primary_key=True)  #id
    tweet_id_str = db.Column(db.String(64), nullable=True) #id_str
    ticker = db.Column(db.String(6), db.ForeignKey('stocks.ticker'))
    date_time = db.Column(db.DateTime, nullable=True)  #created_at
    text = db.Column(db.String(240), nullable=False)  #text
    user = db.Column(db.String(64), nullable=False)  #screen_name
    retweet_count = db.Column(db.Integer, nullable=True)  #retweet_count
    sentiment_str = db.Column(db.String(10), nullable=True)
    sentiment = db.Column(db.Numeric)

    stock = db.relationship('Stock')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "Tweet tweet_id=%s ticker=%s text=%s user=%s>" % (self.tweet_id, self.ticker, self.text, self.user)



##############################################################################
#Creates test database

def example_data():
    """Create some sample data."""

    AAPL = Stock(ticker=AAPL,
                 name='Apple Inc.',
                 sector='Information Technology',
                 industry='Technology Hardware, Storage & Peripherals',
                 correlation=0.6)

    MSFT = Stock(ticker=MSFT,
                 name='Microsoft Corporation',
                 sector='Information Technology',
                 industry='Software',
                 correlation=0.5)

    ORCL = Stock(ticker=ORCL,
                 name='Oracle Corporation',
                 sector='Information Technology',
                 industry='Software',
                 correlation=0.2)

    db.session.add_all([AAPL, MSFT, ORCL])
    db.session.commit()

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lastocks'
    db.app = app
    db.init_app(app)






if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
