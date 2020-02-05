from flask import Flask
from flask import request

import json
import yaml

import qrcode

from PIL import Image, ImageDraw, ImageFont

import re

app = Flask(__name__)

config_file = open('config.yaml', 'r')
config = yaml.load(config_file, Loader=yaml.FullLoader)
BROTHER_QL_PRINTER = config['printer']['model']
BROTHER_QL_MODEL = config['printer']['connection']
LABEL_WIDTH = config['printer']['width']

@app.route('/')
def index():
    return 'Obsługa drukarek etykiet brother'

# curl --header "Content-Type: application/json" --request POST --data '{"id":1463, "supplier_name": "ENDUTEX", "print_material_type": "backlight", "print_material": "Vinyl BP (endutex) niezaciągający wody", "url": "http://192.168.1.100/warehouse_print_materials/1463"}' http://127.0.0.1:5000/api/preview
@app.route("/api/preview", methods=["POST"])
def preview():

    req = request.get_json()
    print(req)

    label_data = jsonToLabel(request.get_json())
    label = label_copy(label_data)
    label.save('./img/test.png')

    return "ok", 200

def label_copy(label):
    img = create_label(label)
    img_2_labels = Image.new('RGB', (696, 2400), color=(255, 255, 255))
    img_2_labels.paste(img, (0, 0))
    img_2_labels.paste(img, (0, 1200))
    return img_2_labels

def create_label(label):
    qr = qrcode.QRCode(box_size=10)
    qr.add_data(label.url)
    qr.make()
    img_qr = qr.make_image()

    fnt = ImageFont.truetype('FreeMonoBold.ttf', 60)
    fnt_bigger = ImageFont.truetype('FreeMonoBold.ttf', 84)

    img_txt = Image.new('RGB', (900, 696), color=(255, 255, 255))
    d_offset = 60
    d = ImageDraw.Draw(img_txt)
    d.text((10, d_offset), 'id: ' + str(label.id), font=fnt_bigger, fill=(0, 0, 0))
    d.text((10, d_offset + 130), label.supplier_name,
           font=fnt_bigger, fill=(0, 0, 0))
    d.text((10, d_offset + 260), label.print_material_type,
           font=fnt_bigger, fill=(0, 0, 0))
    d.text((10, d_offset + 390), re.sub("(.{20})", "\\1\n", label.print_material, 0, re.DOTALL),
           font=fnt, fill=(0, 0, 0))

    img = Image.new('RGB', (696, 1200), color=(255, 255, 255))

    d_id = ImageDraw.Draw(img)
    d_id.text((40, 50), 'ID: ', font=fnt, fill=(0, 0, 0))
    d_id.text((40, 150), str(label.id), font=fnt, fill=(0, 0, 0))

    img.paste(img_qr, (300, 0))
    img.paste(img_txt.rotate(-90, expand=1), (0, 400))

    return img

def jsonToLabel(json):
    label = Label
    label.id = json.get('id')
    label.supplier_name = json.get('supplier_name')
    label.print_material_type = json.get('print_material_type')
    label.print_material = json.get('print_material')
    label.url = json.get('url')
    return label

class Label:
    """
    Custom Label Class
    """

    def __init__(self, id, supplier_name, print_material_type, print_material, url):
        self.id = id
        self.supplier_name = supplier_name
        self.print_material_type = print_material_type
        self.print_material = print_material
        self.url = url

    def __str__(self):
        return self.id
