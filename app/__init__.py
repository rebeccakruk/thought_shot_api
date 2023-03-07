from flask import Flask

app = Flask(__name__)

from endpoints import user, user_login