from flask import Flask
from flask import jsonify
from flask import request

import logging
import sys

from db import DB

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

db = DB()

@app.route('/subscribe', methods=['POST'])
def subscribe():
    user = request.form['user']
    feed = request.form['feed']
    app.logger.info('{} is subscribing to {}'.format(user, feed))
    if not db.subscribe(user, feed):
        return '{} already subscribed to {}'.format(user, feed)

    return '{} successfully subscribed to {}'.format(user, feed)

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    user = request.form['user']
    feed = request.form['feed']
    app.logger.info('{} is unsubscribing from {}'.format(user, feed))
    db.unsubscribe(user, feed)
    return '{} successfully unsubscribed from {}'.format(user, feed)

@app.route('/publish', methods=['POST'])
def publish():
    feed = request.form['feed']
    article = request.form['article']
    app.logger.info('Adding {} to {}'.format(article, feed))
    if not db.add_article_to_feed(article, feed):
        return '{} already in {}'.format(article, feed)

    return 'Successfully published {} to {}'.format(article, feed)

@app.route('/feeds')
def feeds():
    user = request.args.get('user')
    app.logger.info('Requesting feeds for {}'.format(user))
    feeds = db.get_feeds_by_subscriber(user)
    return jsonify(feeds)

@app.route('/articles')
def articles():
    user = request.args.get('user')
    app.logger.info('Requesting articles for {}'.format(user))
    articles = db.get_articles_by_subscriber(user)
    return jsonify(articles)

if __name__ == "__main__":
    app.run()
