import requests
import time
import json
import zmq
from multiprocessing import Process
from logbook import FileHandler, catch_exceptions

####################################### Log book setup #########################
log_handler = FileHandler('collector.log')
log_handler.push_application()


##################################### worker which pulls tweets ################
def worker():
    context = zmq.Context()
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:9999")
    while 1:
        d = json.loads(work_receiver.recv())
        #db.save_doc(doc=d)
        print d['text'], d['user']['geo_enabled'], d['user']['id'],\
        d['user']['lang'], d['user']['created_at'], d['entities'], \
        d['retweet_count']
        

def store_live_tweets():
    Process(target=worker, args=()).start()
    context = zmq.Context()
    send = context.socket(zmq.PUSH)
    send.bind("tcp://127.0.0.1:9999")
    track = ['sachin', 'sachinism', 'Sachin', 'Sachinism', 'tendulkar', 'Tendulkar', 'sachintendulkar','SachinTendulkar']
    while True:
        r = requests.post('https://stream.twitter.com/1/statuses/filter.json',
                    data={'track': track}, auth=('kracetheking', '__import python__'))
        for line in r.iter_lines():
            if line:
                send.send(line)
        else:
            time.sleep(60)            

if __name__ == '__main__':
    with catch_exceptions():
        worker()





