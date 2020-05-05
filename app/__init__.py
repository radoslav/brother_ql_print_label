from flask import Flask
import redis
from rq import Queue

app = Flask(__name__)

r = redis.Redis()
q = Queue('default', connection=r, failure_ttl=3600)

from app import views
