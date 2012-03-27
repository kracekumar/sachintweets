from flask import Flask
app = Flask('sachintweets')
app.secret_key = "1\xf1\x8f\"\x0e\xb2<\x06\xe2\xfa\x9b\x06|0l\xb0\xd6\xdf4\x92\xb3"
import sachintweets.views
