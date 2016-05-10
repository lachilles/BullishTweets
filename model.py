"""Models and database functions for Stock Sentiment project."""


from flask_sqlalchemy import SQLAlchemy

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
    name = db.Column(db.String(64), nullable=False)
    last_px = db.Column(db.Float, nullable=False)
    


    def price_str(self):
        """Return price formatted as string $x.xx"""

        return "$%.2f" % self.price