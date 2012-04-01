from pymongo import Connection
from config import db_username, db_password, db_server, db_port, db_name

#########################make connection here #######################
class MongoException(Exception):
    def __init__(self, error):
        self._msg = error.message

    def __str__(self):
        return repr(self._msg)

def connect():
    connection = Connection(db_server, db_port)
    db = connection[db_name]
    try:
        if db.authenticate(db_username, db_password):
            return db
        else:
            return False
    except Exception as e:
        raise MongoException(e)


def get_top_10_tweets():
    db = connect()
    db = db.tweet
    tweets = db.find({})
    #set limit to ten
    tweets.limit(10)
    top_10_tweets = tweets.sort('retweet_count', -1)#descending order
    to_return = []
    for t in top_10_tweets:
        to_return.append(t)
    return to_return




