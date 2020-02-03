from flask import Flask
import yaml

app = Flask(__name__)

config_file = open('config.yaml', 'r')
config = yaml.load(config_file, Loader=yaml.FullLoader)
BROTHER_QL_PRINTER = config['printer']['model']
BROTHER_QL_MODEL = config['printer']['connection']
LABEL_WIDTH = config['printer']['width']

@app.route('/')
def index():
    return 'Obsługa drukarek etykiet brother'
