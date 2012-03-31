import requests
import time
import json
import zmq
from multiprocessing import Process
from logbook import FileHandler, catch_exceptions
from sachintweets.models import connect, MongoException
from twitter import username, password
from os import remove, getpid

####################################### Log book setup #########################
log_handler = FileHandler('recv.log')
log_handler.push_application()

###################################### Constants ###############################
LOCK_FILE = 'recv.lock'

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
                tweet.insert({'text': d['text'],\
                'location': d['user']['location'], \
                'uid': d['user']['id'], 'tid': d['id'],\
                'created_at': d['user']['created_at'],\
                'username': d['user']['name'],\
                'retweet_count': d['retweet_count']})
                print "===added to db===", d
            else:
                time.sleep(60)
    except Exception as e:
        log_handler.write(e.message)

if __name__ == '__main__':
    with catch_exceptions():
        try:
            with open(LOCK_FILE, 'w') as f:
                f.write(str(getpid()))
            store_live_tweets()
        except IndexError as e:
            log_handler.write(e.message)
        except KeyboardInterrupt:
            log_handler.write('keyboard interrupt\n')
        finally:
            try:
                with open(LOCK_FILE, 'r') as f:
                    #check file exists, I felt this one is better than 
                    #os.path.isfile
                    # http://stackoverflow.com/questions/82831/\
                    #how-do-i-check-if-a-file-exists-using-python
                    pass
                remove(LOCK_FILE)
            except:
                pass




