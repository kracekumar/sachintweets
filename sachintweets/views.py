from flask import render_template, jsonify
from sachintweets import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/realtime')
def real_time_tweets():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://*:6789")
    socket.setsockopt(zmq.SUBSCRIBE, "")
    while 1:
        d = socket.recv() 
        d = json.loads(d)
        return jsonify(text = d['text'], created_at = d['user']['created_at'],\
                       username = d['user']['name'],
                       retweet_count = d['retweet_count'])
