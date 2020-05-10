from flask import render_template, request, redirect
from rq.registry import FailedJobRegistry

from app import app
from app import q
from app.helpers.helper_config import yaml_to_printer
from app.helpers.helper_image import create_imgs_from_labels
from app.helpers.helper_json import jsonToLabels
from app.helpers.helper_printing import is_printer_on
from app.print_task import print_task

printer = yaml_to_printer()


@app.route('/')
def index():
    q_len = len(q)
    jobs = q.jobs

    registry_failed = FailedJobRegistry(queue=q)
    failed_jobs = []
    for job_id in registry_failed.get_job_ids():
        failed_jobs.append(q.fetch_job(job_id))

    return render_template("index.html", jobs=jobs, q_len=q_len, failed_jobs=failed_jobs,
                           failed_len=registry_failed.count)


@app.route("/api", methods=["GET"])
def api():
    return "ok", 200


@app.route("/api/printer_on", methods=["GET"])
def printer_on():
    return str(is_printer_on(printer)), 200


@app.route("/api/failed_clear", methods=["POST"])
def failed_clear():
    registry_failed = FailedJobRegistry(queue=q)
    for job_id in registry_failed.get_job_ids():
        registry_failed.remove(job_id, delete_job=True)
    return redirect("/")


@app.route("/api/requeue", methods=["POST"])
def requeue():
    registry_failed = FailedJobRegistry(queue=q)
    for job_id in registry_failed.get_job_ids():
        registry_failed.requeue(job_id)
    return redirect("/")


@app.route("/api/queue_clear", methods=["POST"])
def queue_clear():
    q.empty()
    return redirect("/")


@app.route("/api/print", methods=["POST"])
def api_print():
    return_dict = {'success': False, 'print_material_ids': []}
    # check for printer on
    if not is_printer_on(printer):  # negation for testing
        # get labels
        labels = jsonToLabels(request.get_json())

        # for each sent to queue
        for label in labels:
            q.enqueue(print_task, printer, label, description=label.id)
            return_dict['print_material_ids'].append(label.id)

        return_dict['message'] = 'printer online!'
        return_dict['success'] = True

    return return_dict, 200


# curl --header "Content-Type: application/json" --request POST --data '[{"id":1463, "supplier_name": "ENDUTEX", "print_material_type": "backlight", "print_material": "Vinyl BP (endutex) niezaciągający wody", "url": "http://192.168.1.100/warehouse_print_materials/1463", "copies":2}]' http://127.0.0.1:5000/api/preview
@app.route("/api/preview", methods=["POST"])
def preview():
    app.logger.warning("dsdsds")
    labels = jsonToLabels(request.get_json())

    imgs = create_imgs_from_labels(labels)
    for i, img in enumerate(imgs):
        img.save('./app/img/test_copy_' + str(i) + '.png')

    return "ok", 200
