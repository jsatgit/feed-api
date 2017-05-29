import logging
import sys

from flask import Flask
from flask import jsonify
from flask import request
from requests import codes

from db import DB

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

db = DB()

@app.route('/reset', methods=['POST'])
def reset():
    app.logger.info('reseting db')
    db.reset()
    return 'Successfully reset database'

@app.route('/subscribe', methods=['POST'])
def subscribe():
    user = request.form['user']
    feed = request.form['feed']
    app.logger.info('{} is subscribing to {}'.format(user, feed))
    if not db.subscribe(user, feed):
        return '{} already subscribed to {}'.format(user, feed), codes.conflict

    return jsonify({'user': user, 'feed': feed}), codes.created

@app.route('/unsubscribe', methods=['DELETE'])
def unsubscribe():
    user = request.form['user']
    feed = request.form['feed']
    app.logger.info('{} is unsubscribing from {}'.format(user, feed))
    db.unsubscribe(user, feed)
    return '', codes.no_content

@app.route('/publish', methods=['POST'])
def publish():
    feed = request.form['feed']
    article = request.form['article']
    app.logger.info('Adding {} to {}'.format(article, feed))
    if not db.add_article_to_feed(article, feed):
        return '{} already in {}'.format(article, feed), codes.conflict

    return jsonify({'feed': feed, 'article': article}), codes.created

@app.route('/feeds')
def feeds():
    user = request.args.get('user')
    app.logger.info('Requesting feeds for {}'.format(user))
    feeds = db.get_feeds_by_subscriber(user)
    return jsonify(feeds), codes.ok

@app.route('/articles')
def articles():
    user = request.args.get('user')
    app.logger.info('Requesting articles for {}'.format(user))
    articles = db.get_articles_by_subscriber(user)
    return jsonify(articles), codes.ok

if __name__ == "__main__":
    app.run()
