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
        tweet = db.tweet
except Exception as e:
    log_handler.write(e.message)


##################################### worker which pulls tweets ################
def worker():
    try:
        context = zmq.Context(1)
        receiver = context.socket(zmq.SUB)
        receiver.connect("tcp://127.0.0.1:9999")
        receiver.setsockopt(zmq.SUBSCRIBE, "t")
        while 1:
             [address, d] = receiver.recv_multipart()
             d = json.loads(d)
             try:
                 if tweet:
                     tweet.insert({'text': d['text'],\
                       'location': d['user']['location'], \
                       'uid': d['user']['id'], 'tid': d['id'],\
                       'created_at': d['user']['created_at'],\
                       'username': d['user']['name'],\
                       'retweet_count': d['retweet_count']})
             except TypeError as e:
                 log_handler.write(MongoException(e))
             except ValueError as e:
                 log_handler.write(MongoException(e))

    except Exception as e:
        log_handler.write(e.message)

def store_live_tweets():
    try:
        Process(target=worker, args=()).start()
        context = zmq.Context(1)
        sender = context.socket(zmq.PUB)
        sender.bind("tcp://*:9999")
        track = ['sachin', 'sachinism', 'Sachin', 'Sachinism', 'tendulkar', 'Tendulkar', 'sachintendulkar','SachinTendulkar']
        while True:
            r = requests.post('https://stream.twitter.com/1/statuses/filter.json',
                    data={'track': track}, auth=(username, password))
            for line in r.iter_lines():
                if line:
                    sender.send_multipart(["t", line])
                    print "===sent==="
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




