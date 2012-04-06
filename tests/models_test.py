from sachintweets.models import connect, get_top_tweets, get_all_tweets,\
                                get_total_tweets
from nose.tools import assert_true, assert_is_instance, assert_false

def test_connect():
    #check connectivity
    assert_true(connect())

def test_get_top_tweets_positive():
    """
        def get_top_tweets(limit = 20):
    """
    assert_is_instance(get_top_tweets(), [])

def test_get_top_tweets_negative():
    """
        def get_top_tweets(limit = 20):
    """
    assert_false(get_top_tweets(limit=-1),[])


    
