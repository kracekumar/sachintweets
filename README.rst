*sachintweets.in* - Fan made site for greatest batsmen Sachin Tendulkar

Working
-------
1. Program connects to twitter(collector.py) and fetches twitter live stream data
   about Sachin Tendulkar and broadcasts using pyzmq.

2. Program which receives all tweets about Sachin Tendulkar(recv.py) and stores 
   the tweets to mongodb.

3. Web App(Flask) serves url .

Install
-------
1. pip install -r requirements.txt

2. `cp twitter_sample.py twitter.py` in project root directory

3. Open the `twitter.py` and enter username and password.

4. `cd sachintweets && cp config.sample config.py` 

5. Open `config.py` add mongodb connection params

6. `cd ..` back to project root directory

7. `nohup python check_process.py >> check_process.out &&`

8. Above command will start `collectory.py` and `recv.py`.

9. It advised to make point `7` as scheduled task.

10. `fabfile.py` to server automation.

11. few log files and output files will be created at run time.

LICENSE
-------
BSD STYLE

Contact me
----------
`Twitter @kracetheking - <http://www.twitter.com/kracetheking>`


