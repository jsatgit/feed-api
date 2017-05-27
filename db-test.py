import sqlite3
from db import DB

db = DB()
db.reset()

alice_feeds = ['Sports', 'Engineering']
bob_feeds = ['Sports', 'Cooking', 'Movies']
charlie_feeds = ['Sports', 'Engineering']

cooking_articles = ['Cooking101', 'How to Bake Bread', 'The Perfect Pasta'] 
engineering_articles = [
    'Kafka: The Definitive Guide',
    'Building Real-Time Data Pipelines',
    'Clean Code'
]
sports_articles = ['How To Run A Marathon']

def get_feeds():
    return (alice_feeds[:], bob_feeds[:], charlie_feeds[:])

def get_articles():
    return (cooking_articles[:], engineering_articles[:], sports_articles[:])

def subscribe_user_to_feeds(user, feeds):
    for feed in feeds:
        db.subscribe(user, feed)

def add_articles_to_feed(feed, articles):
    for article in articles:
        db.add_article_to_feed(article, feed)

def assert_lst(a, b):
    assert sorted(a) == sorted(b)

def test_subscribe():
    alice_feeds, bob_feeds, charlie_feeds = get_feeds()
    subscribe_user_to_feeds('Alice', alice_feeds)
    subscribe_user_to_feeds('Bob', bob_feeds)
    subscribe_user_to_feeds('Charlie', charlie_feeds)

    assert_lst(db.get_feeds_by_subscriber('Alice'), alice_feeds)
    assert_lst(db.get_feeds_by_subscriber('Bob'), bob_feeds)
    assert_lst(db.get_feeds_by_subscriber('Charlie'), charlie_feeds)

def test_add_articles_to_feeds():
    cooking_articles, engineering_articles, sports_articles = get_articles()
    add_articles_to_feed('Cooking', cooking_articles)
    add_articles_to_feed('Engineering', engineering_articles)
    add_articles_to_feed('Sports', sports_articles)

    assert_lst(db.get_articles_by_subscriber('Alice'), engineering_articles + sports_articles)

def test_unsubscribe():
    alice_feeds, bob_feeds, charlie_feeds = get_feeds()
    alice_feeds.remove('Sports')
    bob_feeds.remove('Cooking')
    db.unsubscribe('Alice', 'Sports')
    db.unsubscribe('Bob', 'Cooking')

    assert_lst(db.get_feeds_by_subscriber('Alice'), alice_feeds)
    assert_lst(db.get_feeds_by_subscriber('Bob'), bob_feeds)

def test_dup_subscribe():
    alice_feeds, bob_feeds, charlie_feeds = get_feeds()
    subscribe_user_to_feeds('Alice', alice_feeds)
    assert db.subscribe('Alice', alice_feeds[0]) == False

def test_dup_articles_in_feed():
    cooking_articles, engineering_articles, sports_articles = get_articles()
    add_articles_to_feed('Cooking', cooking_articles)
    assert db.add_article_to_feed(cooking_articles[0], 'Cooking') == False

test_subscribe()
test_add_articles_to_feeds()
test_unsubscribe()
db.reset()
test_dup_subscribe()
test_dup_articles_in_feed()
