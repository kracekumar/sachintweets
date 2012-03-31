import requests
import time
import zmq
from logbook import FileHandler, catch_exceptions
from twitter import username, password

####################################### Log book setup #########################
log_handler = FileHandler('collector.log')
log_handler.push_application()

###################################### Zero MQ set up for psuh #################
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:6789")

def collect_tweets():
    try:
        track = ['sachin', 'sachinism', 'Sachin', 'Sachinism', 'tendulkar', 'Tendulkar', 'sachintendulkar','SachinTendulkar']
        while True:
            r = requests.post('https://stream.twitter.com/1/statuses/filter.json',
                    data={'track': track}, auth=(username, password))
            for line in r.iter_lines():
                if line:
                    socket.send(line)
                    print "====sent====="
            else:
                time.sleep(60)
    except Exception as e:
        log_handler.write(e.message)

if __name__ == '__main__':
    with catch_exceptions():
        try:
            collect_tweets()
        except IndexError as e:
            log_handler.write(e.message)
        except KeyboardInterrupt:
            log_handler.write('keyboard interrupt\n')




