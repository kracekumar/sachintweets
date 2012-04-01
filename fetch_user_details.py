import requests
import time
import json
import zmq
from logbook import FileHandler, catch_exceptions
from sachintweets.models import connect, MongoException

####################################### Log book setup #########################
log_handler = FileHandler('fetch_user_details.log')
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


def fetch_user_details():
    tweets = tweet.find({})
    for t in tweets:
        if not 'screen_name' in t:
            r = requests.get("http://api.twitter.com/1/statuses/show/%d.json"\
            %(t['tid']))
            d = json.loads(r.content)
            if 'user' in d:
                tweet.update({'tid': t['tid']},{'$set': {
                'screen_name': d['user']['screen_name'],\
                'profile_image_url': d['user']['profile_image_url']}})
                print "%s ===updated to db=== %d", time.ctime(), t['tid']

if __name__ == '__main__':
    fetch_user_details()




