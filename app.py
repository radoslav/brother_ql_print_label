from flask import Flask
import yaml
from flask import request

app = Flask(__name__)

config_file = open('config.yaml', 'r')
config = yaml.load(config_file, Loader=yaml.FullLoader)
BROTHER_QL_PRINTER = config['printer']['model']
BROTHER_QL_MODEL = config['printer']['connection']
LABEL_WIDTH = config['printer']['width']

@app.route('/')
def index():
    return 'Obsługa drukarek etykiet brother'

# curl --header "Content-Type: application/json" --request POST --data '{"id":1, "supplier_name": "igepa", "print_material_type": "baner", "print_material": "frontlight", "url": "http://google.pl"}' http://127.0.0.1:5000/api/preview
@app.route("/api/preview", methods=["POST"])
def preview():

    req = request.get_json()

    print(req)

    return "ok", 200