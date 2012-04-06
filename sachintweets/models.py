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
    except Exception as e:
        raise MongoException(e)


def get_top_tweets(limit = 20):
    if limit >= 0:
        db = connect()
        top_tweets = db.tweet.find().sort('retweet_count', -1)#descending order
        to_return = []
        check = {}
        for t in top_tweets:
            if len(check) == limit:
                break
            else:
                if t['text'] not in check:
                    check[t['text']] = 1
                    to_return.append(t)
        return to_return
    else:
        return False

def get_all_tweets(limit=20, skip=0):
    if limit >=0 and skip >= 0:
        db = connect()
        db = db.tweet
        tweets = db.find({}).skip(skip).limit(limit).sort('created_at', -1)
        to_return = []
        for t in tweets:
            to_return.append(t)
        return to_return
    else:
        return False


def get_total_tweets():
    db = connect()
    return db.tweet.count()
