#! /usr/bin/env python
from os import system
"""
    This file is intended as cron job to check whether collector.py and recv.py
    is running, if not start collector.py or recv.py 
"""

RECV_LOCK_FILE = 'recv.lock'
COLLECTOR_LOCK_FILE = 'collector.lock'

def check():
    try:
        with open(COLLECTOR_LOCK_FILE) as f:
            pass
    except:
        system("nohup python2.7 collector.py >> collector.out &")
        print "===started collector.py==="
    try:
        with open(RECV_LOCK_FILE) as f:
            pass
    except:
        system("nohup python2.7 recv.py >> recv.out &")
        print "===started recv.py==="


if __name__ == "__main__":
    check()
    
