from flask import Flask
from flask import request

import json
import yaml

import qrcode

from PIL import Image, ImageDraw, ImageFont

import re

from io import BytesIO

from brother_ql.devicedependent import models, label_type_specs, label_sizes
# from brother_ql.devicedependent import ENDLESS_LABEL, DIE_CUT_LABEL, ROUND_DIE_CUT_LABEL
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend


class Printer:
    """
    Custom Printer Class
    """

    def __init__(self, model, connection, width):
        self.model = model
        self.connection = connection
        self.width = width

    def __str__(self):
        return self.model


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


def label_copy(label):
    img = label_img(label)
    img_2_labels = Image.new('RGB', (696, 2400), color=(255, 255, 255))
    img_2_labels.paste(img, (0, 0))
    img_2_labels.paste(img, (0, 1200))
    return img_2_labels


def label_img(label):
    qr = qrcode.QRCode(box_size=10)
    qr.add_data(label.url)
    qr.make()
    img_qr = qr.make_image()

    fnt = ImageFont.truetype('FreeMonoBold.ttf', 60)
    fnt_bigger = ImageFont.truetype('FreeMonoBold.ttf', 84)

    img_txt = Image.new('RGB', (900, 696), color=(255, 255, 255))
    d_offset = 60
    d = ImageDraw.Draw(img_txt)
    d.text((10, d_offset), 'id: ' + str(label.id),
           font=fnt_bigger, fill=(0, 0, 0))
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


def yaml_to_printer():
    config_file = open('config.yaml', 'r')
    config = yaml.load(config_file, Loader=yaml.FullLoader)
    printer = Printer
    printer.model = config['printer']['model']
    printer.connection = config['printer']['connection']
    printer.width = config['printer']['width']
    return printer


def image_to_png_bytes(im):
    image_buffer = BytesIO()
    im.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    return image_buffer.read()


app = Flask(__name__)

printer = yaml_to_printer()

selected_backend = guess_backend(printer.connection)
BACKEND_CLASS = backend_factory(selected_backend)['backend_class']

@app.route('/')
def index():
    return 'Obsługa drukarek etykiet brother'


@app.route("/api/print", methods=["POST"])
def print():
    label_data = jsonToLabel(request.get_json())
    image = label_img(label_data)

    # from brother_ql
    qlr = BrotherQLRaster(printer.model)
    
    create_label(qlr, image, printer.width, threshold=70, cut=True, dither=False, compress=False, red=False)

    return_dict = {'success': False}

    try:
        be = BACKEND_CLASS(printer.connection)
        be.write(qlr.data)
        be.dispose()
        del be
    except Exception as e:
        return_dict['message'] = str(e)

    return return_dict, 200

# curl --header "Content-Type: application/json" --request POST --data '{"id":1463, "supplier_name": "ENDUTEX", "print_material_type": "backlight", "print_material": "Vinyl BP (endutex) niezaciągający wody", "url": "http://192.168.1.100/warehouse_print_materials/1463"}' http://127.0.0.1:5000/api/preview
@app.route("/api/preview", methods=["POST"])
def preview():

    label_data = jsonToLabel(request.get_json())
    label = label_copy(label_data)
    label.save('./img/test.png')

    return "ok", 200
