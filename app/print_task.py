import time


def print_task(label):
    time.sleep(5)

    raise NameError('HiThere')
    return True

#
# @app.route("/api/print", methods=["POST"])
# def api_print():
#     label_data = jsonToLabels(request.get_json())
#
#     image = img_label(label_data)
#
#     # from brother_ql
#     qlr = BrotherQLRaster(printer.model)
#
#     create_label(qlr, image, printer.width, threshold=70, cut=True, dither=False, compress=False, red=False)
#
#     return_dict = {'success': False}
#
#     try:
#         be = BACKEND_CLASS(printer.connection)
#         be.write(qlr.data)
#         be.dispose()
#         del be
#     except Exception as e:
#         return_dict['message'] = str(e)
#
#     return return_dict, 200
