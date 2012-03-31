<<ABOUT
    shell script to start collector.py and recv.py
    primarily written to save typing
    this file will also be executed using nohup ./start.sh&
ABOUT
nohup python2.7 collector.py&
sleep 1
nohup python2.7 recv.py&

