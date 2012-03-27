from sqlalchemy import create_engine, Column, BigInteger, String, Sequence, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import db_username, db_password, db_name, db_server
from datetime import datetime

#################### Create Engine #################################

engine = create_engine('postgresql://%s:%s@%s/%s'%(db_username, db_password,\
                                                   db_server, db_name))

Base = declarative_base()

class Tweets(Base):
    __tablename__ = 'sachin_tweets'
    
    """
        sid: sequence id
        text: actual tweet, d['tweet']
        retweet_count: no of times retweeted, d['retweet_count']
        location: location of the tweeter, d['user']['location']
        uid: userid, d['user']['id']
        tid: tweet id, d['id']
        created_at: tweet creation date, t['created_at']
        username: tweeter name, d['user']['name']
        inserted_at: time when tweet was inserted into db
    """
    sid = Column(BigInteger, Sequence('sid_seq'), primary_key = True)
    text = Column(String, nullable=False)
    retweet_count = Column(BigInteger, nullable=False)
    location = Column(String, nullable=False)
    uid = Column(BigInteger, nullable=False)
    tid = Column(BigInteger, nullable=False)
    created_at = Column(String, nullable=False)
    username = Column(String, nullable=False)
    inserted_at = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, sid, text, retweet_count, location, uid, tid, \
                 created_at, username, inserted_at):
        self.sid = sid
        self.text = text
        self.retweet_count = retweet_count
        self.location = location
        self.uid = uid
        self.tid = tid
        self.created_at = created_at
        self.username = username
        self.inserted_at = insert_at

    def __repr__(self):
        return"<Tweet: %s by %s>"%(self.text, self.username)

class Count(Base):
    __tablename__ = 'count'

    """
        cid: count id, total tweets on a particular day
        total_count: total no of tweets on particluar day 
        date: every day
    """
    cid = Column(BigInteger, Sequence('count_seq'), primary_key=True)
    total_count = Column(BigInteger, nullable = False)
    date = Column(Date, nullable = False, unique=True)

    def __init__(self, total_count, date):
        self.total_count = total_count
        self.date = date

    def __repr__(self):
        return "<Count: On %s %s people tweeted>"%(self.total_count, self.date)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

