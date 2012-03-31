import requests
import time
import json
import zmq
from multiprocessing import Process
from logbook import FileHandler, catch_exceptions
from sachintweets.models import connect, MongoException
from twitter import username, password

####################################### Log book setup #########################
log_handler = FileHandler('collector.log')
log_handler.push_application()

###################################### Mongodb connection ######################
try:
    db =  connect() 
    if db:
       tweet  = db.tweet
except Exception as e:
    log_handler.write(e.message)

#################################### ZERO MQ PULLER ############################
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://*:6789")
socket.setsockopt(zmq.SUBSCRIBE, "")


def store_live_tweets():
    try:
        while True:
            d = json.loads(socket.recv())
            if tweet:
                tweet.insert({'text': line['text'],\
                'location': line['user']['location'], \
                'uid': line['user']['id'], 'tid': line['id'],\
                'created_at': line['user']['created_at'],\
                'username': line['user']['name'],\
                'retweet_count': line['retweet_count']})
                 print "===added to db===", line
            else:
                time.sleep(60)
    except Exception as e:
        log_handler.write(e.message)

if __name__ == '__main__':
    with catch_exceptions():
        try:
            store_live_tweets()
        except IndexError as e:
            log_handler.write(e.message)
        except KeyboardInterrupt:
            log_handler.write('keyboard interrupt\n')




