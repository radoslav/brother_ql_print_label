from flask import Flask

import json
import yaml

import qrcode

from PIL import Image, ImageDraw, ImageFont

import re

from io import BytesIO

import brother_ql.models  
import brother_ql.labels
# from brother_ql.devicedependent import ENDLESS_LABEL, DIE_CUT_LABEL, ROUND_DIE_CUT_LABEL
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend

import usb.core

import time

# redis and rq for queue
import redis
from rq import Queue

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

from app import views
from app import models

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

    array_id = re.findall("[0-9a-fA-F]{4}", printer.connection)
    if array_id:
        printer.idVendor = array_id[0]
        printer.idProduct = array_id[1]

    return printer


def image_to_png_bytes(im):
    image_buffer = BytesIO()
    im.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    return image_buffer.read()

def is_printer_on(printer):
    dev = usb.core.find(idVendor=printer.idVendor, idProduct=printer.idProduct)
    if dev:
        return True
    else:
            return False

printer = yaml_to_printer()

selected_backend = guess_backend(printer.connection)
BACKEND_CLASS = backend_factory(selected_backend)['backend_class']


def background_task(n):

    """ Function that returns len(n) and simulates a delay """

    delay = 2

    print("Task running")
    print(f"Simulating a {delay} second delay")

    time.sleep(delay)

    print(len(n))
    print("Task complete")

    return len(n)

