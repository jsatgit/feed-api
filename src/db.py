import sqlite3

class DB:
    def __init__(self):
        self.connection = sqlite3.connect('feed.db')
        self.cursor = self.connection.cursor()

    def reset(self):
        self.cursor.executescript(
            '''
            DROP TABLE IF EXISTS subscriber;
            CREATE TABLE subscriber (
                user varchar(50) not null,
                feed varchar(50) not null,
                UNIQUE (user, feed)
            );

            DROP TABLE IF EXISTS subscription;
            CREATE TABLE subscription (
                feed varchar(50) not null,
                article varchar(50) not null,
                UNIQUE (feed, article)
            );
            '''
        )
        self.connection.commit()

    def subscribe(self, user, feed):
        try:
            self.cursor.execute(
                '''
                INSERT INTO subscriber (user, feed)
                VALUES (?, ?)
                ''', (user, feed)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            return False

        return True

    def unsubscribe(self, user, feed):
        self.cursor.execute(
            '''
            DELETE FROM subscriber
            WHERE user=? and feed=?
            ''', (user, feed)
        )
        self.connection.commit()

    def add_article_to_feed(self, article, feed):
        try:
            self.cursor.execute(
                '''
                INSERT INTO subscription (feed, article)
                VALUES (?, ?)
                ''' , (feed, article)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            return False

        return True

    def get_feeds_by_subscriber(self, user):
        self.cursor.execute(
            '''
            SELECT feed FROM subscriber
            WHERE user=?
            ''', (user, )
        )
        self.connection.commit()
        return [feed for feed, in self.cursor.fetchall()]

    def get_articles_by_subscriber(self, user):
        self.cursor.execute(
            '''
            SELECT article FROM subscription
            WHERE feed IN (
                SELECT feed FROM subscriber
                WHERE user=? 
            )
            ''', (user, )
        )
        self.connection.commit()
        return [article for article, in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()
        self.connection.close()
