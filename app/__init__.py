from flask import Flask

# redis and rq for queue
import redis
from rq import Queue
r = redis.Redis()
q = Queue(connection=r)

app = Flask(__name__)
from app import views

from app.printing import yaml_to_printer
from brother_ql.backends import backend_factory, guess_backend

printer = yaml_to_printer()
selected_backend = guess_backend(printer.connection)
BACKEND_CLASS = backend_factory(selected_backend)['backend_class']

