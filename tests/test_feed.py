import unittest
import json
import requests

from requests import codes

import mock_data

base_url = 'http://localhost:5000'

def subscribe(request_data):
    return requests.post(
        base_url + '/subscribe',
        data=request_data
    )

def bulk_subscribe(request_data):
    for request in request_data:
        subscribe(request)

def publish(request_data):
    return requests.post(
        base_url + '/publish',
        data=request_data
    )

def bulk_publish(request_data):
    for request in request_data:
        publish(request)

class TestFeed(unittest.TestCase):
    def setUp(self):
        requests.post(base_url + '/reset')

    def test_subscribe(self):
        request_data = {'user': 'James', 'feed': 'Engineering'}
        response = subscribe(request_data)
        self.assertEqual(response.status_code, codes.created)
        self.assertEqual(json.loads(response.text), request_data)

    def test_unsubscribe(self):
        request_data = {'user': 'James', 'feed': 'Engineering'}
        subscribe(request_data)
        response = requests.delete(
            base_url + '/unsubscribe',
            data=request_data
        )
        self.assertEqual(response.status_code, codes.no_content)
        self.assertEqual(response.text, '')

    def test_publish(self):
        request_data = {'feed': 'Engineering', 'article': mock_data.articles['Engineering'][0]}
        response = publish(request_data)
        self.assertEqual(response.status_code, codes.created)
        self.assertEqual(json.loads(response.text), request_data)

    def test_feeds(self):
        user_feeds = [
            {'user': 'James', 'feed': 'Engineering'},
            {'user': 'James', 'feed': 'Cooking'}
        ]
        bulk_subscribe(user_feeds) 
        response = requests.get(
            base_url + '/feeds',
            params={'user': 'James'}
        )
        self.assertEqual(response.status_code, codes.ok)
        self.assertItemsEqual(
            json.loads(response.text),
            [user_feed['feed'] for user_feed in user_feeds]
        )

    def test_articles(self):
        bulk_subscribe([
            {'user': 'James', 'feed': 'Engineering'},
            {'user': 'James', 'feed': 'Cooking'}
        ])
        feed_articles = [
            {'feed': 'Engineering', 'article': mock_data.articles['Engineering'][0]},
            {'feed': 'Cooking', 'article': mock_data.articles['Cooking'][0]},
            {'feed': 'Cooking', 'article': mock_data.articles['Cooking'][1]}
        ]
        bulk_publish(feed_articles)
        response = requests.get(
            base_url + '/articles',
            params={'user': 'James'}
        )
        self.assertEqual(response.status_code, codes.ok)
        self.assertItemsEqual(
            json.loads(response.text),
            [feed_article['article'] for feed_article in feed_articles]
        )

if __name__ == '__main__':
    unittest.main()
