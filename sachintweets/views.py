from flask import render_template, jsonify
from sachintweets import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/realtime')
def real_time_tweets():
    context = zmq.Context(1)
    receiver = context.socket(zmq.SUB)
    receiver.connect("tcp://127.0.0.1:9999")
    receiver.setsockopt(zmq.SUBSCRIBE, "t")
    while 1:
        [address, d] = receiver.recv_multipart()
        d = json.loads(d)
        return jsonify(text = d['text'], created_at = d['user']['created_at'],\
                       username = d['user']['name'],
                       retweet_count = d['retweet_count'])
