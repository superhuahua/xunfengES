import sys
import os
from datetime import timedelta
from flask import Flask
from Config import ServerConfig

app = Flask(__name__)
app.secret_key = "\xe8\xf7\xb9\xae\xfb\x87\xea4<5\xe7\x97D\xf4\x88)Q\xbd\xe1j'\x83\x13\xc7"
app.config.from_object(ServerConfig)
app.debug=True

app.permanent_session_lifetime = timedelta(hours=6)


