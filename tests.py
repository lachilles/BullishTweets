import unittest
from unittest import TestCase
from model import Stock, Tweet, example_data, connect_to_db, db
from server import app
import server


class FlaskTestsBasic(unittest.TestCase):
    """Tests for my app"""

    def setUp(self):
         # Get the Flask test client
        self.client = server.app.test_client()
        # Show Flask errors that happen during tests
        server.app.config['TESTING'] = True

    def test_homepage(self):
        #Checks that the h1 is rendering in homepage.html
        result = self.client.get("/")
        self.assertIn("<h1>BullishTweets</h1>", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///lastocks")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_bar_graph(self):
        """Test create_bar_graph."""

        result = self.client.get("/data.json")
        self.assertIn("?", result.data)

    def test_scatter_graph(self):
        """Test scatter_graph."""

        result = self.client.get("/scatterdata.json")
        self.assertIn("?", result.data)

if __name__ == "__main__":
    unittest.main()
