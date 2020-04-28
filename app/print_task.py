import time


def print_task(label):
    time.sleep(5)

    # raise NameError('HiThere')
    return True

#
# def send_img_to_printer(printer, img):
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
