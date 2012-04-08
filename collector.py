import requests
import time
import zmq
from logbook import FileHandler, catch_exceptions
from twitter import username, password
from os import getpid, remove

####################################### Log book setup #########################
log_handler = FileHandler('collector.log')
log_handler.push_application()

###################################### Zero MQ set up for push #################
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:6789")

##################################### constants ###############################
LOCK_FILE = 'collector.lock'


###################################### core ####################################
def collect_tweets():
    while True:
        try:
            track = ['sachin', 'sachinism', 'Sachin', 'Sachinism', 'tendulkar', 'Tendulkar', 'sachintendulkar','SachinTendulkar']
            r = requests.post('https://stream.twitter.com/1/statuses/filter.json',
                    data={'track': track}, auth=(username, password))
            for line in r.iter_lines(chunk_size=2048):
                if line:
                    socket.send(line)
                    print "%s ====sent====="%time.ctime()
            else:
                time.sleep(60)
        except Exception as e:
            log_handler.write(e.message)

if __name__ == '__main__':
    with catch_exceptions():
        try:
            with open(LOCK_FILE, 'w') as f:
                f.write(str(getpid()))
            collect_tweets()
        except IndexError as e:
            log_handler.write(e.message)
        except KeyboardInterrupt:
            log_handler.write('keyboard interrupt\n')
        finally:
            try:
                with open(LOCK_FILE, 'r') as f:
                    pass
                remove(LOCK_FILE)
            except:
                pass
            



