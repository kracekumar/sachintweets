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



