from flask import Flask
import yaml

app = Flask(__name__)

config_file = open('config.yaml', 'r')
config = yaml.load(config_file, Loader=yaml.FullLoader)

@app.route('/')
def index():
    return 'Obsługa drukarek etykiet brother' + config['foo']
