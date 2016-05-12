"""Utility file to seed stock data from S&P 500 constituents in seed_data/"""

# from sqlalchemy import func
from model import Stock
# from model import Stock

from model import connect_to_db, db
from server import app

# import datetime

def load_stocks():
    """Load stocks from SPX_constituents into database."""

    print "Stocks"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Stock.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/SPX_constituents.txt"):
        row = row.strip()
        print row
        ticker, name, sector, industry = row.split("\t")

        stock = Stock(ticker=ticker,
                    name=name,
                    sector=sector,
                    industry=industry)

        # We need to add to the session or it won't ever be stored
        db.session.add(stock)

    # Once we're done, we should commit our work
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_stocks()
