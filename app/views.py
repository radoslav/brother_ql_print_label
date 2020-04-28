from brother_ql import BrotherQLRaster, create_label

from app import app
from app import q

from flask import render_template, request

from app.helper_config import yaml_to_printer
from app.helper_image import jsonToLabel, label_img, label_copy
from app.helper_printing import is_printer_on

from brother_ql.backends import backend_factory, guess_backend

from app.print_task import print_task

printer = yaml_to_printer()

selected_backend = guess_backend(printer.connection)
BACKEND_CLASS = backend_factory(selected_backend)['backend_class']

@app.route('/')
def index():
    q_len = len(q)
    jobs = q.jobs
    return render_template("index.html", jobs=jobs, q_len=q_len)

@app.route("/api", methods=["GET"])
def api():

    return "ok", 200

@app.route("/api/printer_on", methods=["GET"])
def printer_on():
    return str(is_printer_on(printer)), 200

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
    app.logger.warning("dsdsds")
    label_data = jsonToLabel(request.get_json())
    label = label_copy(label_data)
    label.save('./app/img/test.png')

    task = q.enqueue(print_task, label_data, description='test')

    message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {len(q)} jobs queued"
    print(message)

    return "ok", 200
