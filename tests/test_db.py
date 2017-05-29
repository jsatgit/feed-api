import sqlite3
import unittest

import src
from src.db import DB
from mock_data import get_mock_feeds
from mock_data import get_mock_articles

class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DB()

    def subscribe_user_to_feeds(self, user, feeds):
        for feed in feeds:
            self.db.subscribe(user, feed)

    def add_articles_to_feed(self, feed, articles):
        for article in articles:
            self.db.add_article_to_feed(article, feed)

    def setUp(self):
        self.db.reset()

    def test_subscribe(self):
        alice_feeds, bob_feeds, charlie_feeds = get_mock_feeds()
        self.subscribe_user_to_feeds('Alice', alice_feeds)
        self.subscribe_user_to_feeds('Bob', bob_feeds)
        self.subscribe_user_to_feeds('Charlie', charlie_feeds)

        self.assertItemsEqual(self.db.get_feeds_by_subscriber('Alice'), alice_feeds)
        self.assertItemsEqual(self.db.get_feeds_by_subscriber('Bob'), bob_feeds)
        self.assertItemsEqual(self.db.get_feeds_by_subscriber('Charlie'), charlie_feeds)

    def test_unsubscribe(self):
        alice_feeds, bob_feeds, charlie_feeds = get_mock_feeds()
        self.subscribe_user_to_feeds('Alice', alice_feeds)
        self.subscribe_user_to_feeds('Bob', bob_feeds)

        self.db.unsubscribe('Alice', 'Sports')
        self.db.unsubscribe('Bob', 'Cooking')

        alice_feeds.remove('Sports')
        bob_feeds.remove('Cooking')

        self.assertItemsEqual(self.db.get_feeds_by_subscriber('Alice'), alice_feeds)
        self.assertItemsEqual(self.db.get_feeds_by_subscriber('Bob'), bob_feeds)

    def test_add_articles_to_feeds(self):
        alice_feeds, bob_feeds, charlie_feeds = get_mock_feeds()
        self.subscribe_user_to_feeds('Alice', alice_feeds)

        cooking_articles, engineering_articles, sports_articles = get_mock_articles()
        self.add_articles_to_feed('Cooking', cooking_articles)
        self.add_articles_to_feed('Engineering', engineering_articles)
        self.add_articles_to_feed('Sports', sports_articles)

        self.assertItemsEqual(self.db.get_articles_by_subscriber('Alice'), engineering_articles + sports_articles)

    def test_dup_subscribe(self):
        alice_feeds, bob_feeds, charlie_feeds = get_mock_feeds()
        self.subscribe_user_to_feeds('Alice', alice_feeds)
        self.assertFalse(self.db.subscribe('Alice', alice_feeds[0]))

    def test_dup_articles_in_feed(self):
        cooking_articles, engineering_articles, sports_articles = get_mock_articles()
        self.add_articles_to_feed('Cooking', cooking_articles)
        self.assertFalse(self.db.add_article_to_feed(cooking_articles[0], 'Cooking'))

    def test_persist(self):
        alice_feeds, bob_feeds, charlie_feeds = get_mock_feeds()
        self.subscribe_user_to_feeds('Alice', alice_feeds)
        self.db.close()
        TestDB.db = DB()
        self.assertItemsEqual(self.db.get_feeds_by_subscriber('Alice'), alice_feeds)


if __name__ == '__main__':
    unittest.main()
