# Feed Api

Feed Api is a HTTP service that provides the following functionality:

1. Subscribe/Unsubscribe a User to a Feed
2. Add Articles to a Feed
3. Get all Feeds a Subscriber is following
4. Get Articles from the set of Feeds a Subscriber is following

## Getting Started

Follow these instructions to get feed api running locally

### Prerequisites

* Python 2.7
* pip
* virtualenv
* SQLite3

### Installing

1. Create a virtual environment in the project root directory:
```
virtualenv venv
```

2. Install the python libraries:
```
pip install -r requirements.txt
```

### Starting service

While virtualenv is activated run:
```
make start
```

This will start the service on `localhost:5000`

### Example queries

Subscribe the user "James" to the "Cooking" feed
```
curl --data "user=James&feed=Cooking" http://localhost:5000/subscribe
```

Publish the article "Cooking101" to the "Cooking" feed
```
curl --data "feed=Cooking&article=Cooking101" http://localhost:5000/publish
```

List the feeds that the user "James" has subscribed to
```
curl "http://localhost:5000/feeds?user=James"
```

## Tests

Start the service then run the tests:
```
make start
make test
```

## API Reference

Method | Name | Fields | Description 
--- | --- | --- | ---
POST | subscribe | user, feed | subscribe a user to a feed
DELETE | unsubscribe | user, feed | unsubscribe a user from a feed
POST | publish | feed, article | publish an article to a feed
GET | feeds | user | list feeds a user has subscribed to
GET | articles | user | list articles from all the feeds a user has subscribed to

## Structure of service

There are two components of this service. A web application component and a database component.

### Major Dependencies 

1. [Flask](http://flask.pocoo.org/) - Flask is used as the web application framework. It is responsible for handling concurrent HTTP requests
with custom Python code. Flask was chosen because it has a clean interface and it gives the developer freedom to choose custom database tools.

3. [SQLite](https://www.sqlite.org/) - SQLite is used as a database to support data persistence. A relational database was chosen because the relationship
between users, feeds, articles can be easily expressed and queried using this model. SQLite was used instead of MySQL or Postgres since 
it is lightweight and the higher concurrency aspects of client/server databases are of lower priority at the moment. 

### Database Schema

#### subscriber

Column | Type
--- | ---
user | char(50)
feed | char(50)

#### subscription
Column | Type
--- | ---
feed | char(50)
article | char(50)

### Limitations and Future Considerations

Currently, only relationships are represented as tables in the database. This is sufficient for the current set of operations.
In a more realistic scenario, an article will contain more fields than just a name. 
For example, it will also contain fields for its author and content. 
To support this extension a new table can be created for an article.
In addition, this requires opening up another API endpoint for creating articles. 
On the database end, a primary key can be added to the article table so that articles in 
relationship tables can refer to articles by their primary keys. A similar extension applies 
to other entities such as feeds and users.

The current API does not allow for bulk operations. Users sometimes may want to subscribe to more than one feed
at once. Providing the ability to allow for bulk submission will lead to less network requests.

A proper web server such as Nginx has not been set up since this service is not being productionized at the moment.

A client/server database such as MySQL would be more appropriate if we wanted to scale to more concurrent users.
