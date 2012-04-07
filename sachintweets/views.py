from flask import render_template, jsonify, Response
from sachintweets import app
from models import get_top_tweets, get_all_tweets, get_total_tweets
import zmq
import json

####################### ZMQ for sending real time tweets to client #############

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://*:6789")
socket.setsockopt(zmq.SUBSCRIBE, "")

########################################### helpers ############################
def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv  = t.stream(context)
    rv.enable_buffering(5)
    return rv

################################################# func to URL ##################
@app.route('/')
def index():
    tweets = get_top_tweets(limit=25)
    return render_template('index.html', tweets = tweets)

@app.route('/tweets/<int:page_no>/')
def tweets(page_no):
    if page_no == 1:
        skip = 0
    else:
        if page_no > 1:
            skip = page_no * 24
        else:
            return render_template('error.html', msg=msg)
    tweets = get_all_tweets(limit=25, skip=skip)
    total_tweets = get_total_tweets()
    if total_tweets % 25 :
        total = (total_tweets /25 ) + 1
    else:
        total = total_tweets / 25
    return render_template('tweets.html', tweets = tweets, total = total, \
                            page_no = page_no)

@app.route('/total_tweet/')
def total():
    return jsonify(total = get_total_tweets())

@app.route('/realtime/pull/')
def real_time_tweets_pull():
    d = socket.recv() 
    d = json.loads(d)
    return jsonify(text = d['text'], created_at = d['user']['created_at'],\
                       username = d['user']['name'],
                       retweet_count = d['retweet_count'])
    
@app.route('/realtime/')
def realtime_update():
    return render_template('realtime.html')
