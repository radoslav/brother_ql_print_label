from flask import Flask
from flask import request
import yaml
import qrcode
from PIL import Image, ImageDraw, ImageFont

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

    qr = qrcode.QRCode(box_size=10)
    qr.add_data('http://google.pl')
    qr.make()
    img_qr = qr.make_image()

    fnt = ImageFont.truetype('FreeMonoBold.ttf', 60)
    fnt_bigger = ImageFont.truetype('FreeMonoBold.ttf', 84)

    img_txt = Image.new('RGB', (900, 696), color = (255, 255, 255))
    d_offset = 60
    d = ImageDraw.Draw(img_txt)
    d.text((10, d_offset ), "ID: ", font=fnt_bigger, fill=(0,0,0))
    d.text((10, d_offset + 150), "fdfsdfsdf: ", font=fnt_bigger, fill=(0,0,0))
    d.text((10, d_offset + 300), "fdfsdfsdf: ", font=fnt_bigger, fill=(0,0,0))
    d.text((10, d_offset + 450), "fdfsdfsdf: ", font=fnt_bigger, fill=(0,0,0))

    img = Image.new('RGB', (696, 1200), color = (255, 255, 255))

    d_id = ImageDraw.Draw(img)
    d_id.text((10, 150 ), "ID: ", font=fnt, fill=(0,0,0))

    img.paste(img_qr, (350,0))
    img.paste(img_txt.rotate(-90, expand=1), (0,320))

    img.save('./img/pil_text.png')

    return "ok", 200
