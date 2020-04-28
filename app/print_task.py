import time

from app.helpers.helper_image import img_label


def print_task(label):
    time.sleep(5)

    # raise NameError('HiThere')
    return True


def create_imgs_from_labels(labels):
    imgs = []
    for label in labels:
        img = img_label(label)
        imgs.append(img)
    return imgs


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
