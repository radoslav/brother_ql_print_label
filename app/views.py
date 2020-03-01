from app import app
from app import r
from app import q

from flask import render_template, request

import json
from app import models

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/api/print", methods=["POST"])
def api_print():
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
    label.save('./app/img/test.png')

    return "ok", 200
