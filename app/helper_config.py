import re

import yaml

from app.models import Printer


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
