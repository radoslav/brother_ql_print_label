from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend

from app.helpers.helper_image import img_label


def print_task(printer, label):
    selected_backend = guess_backend(printer.connection)
    BACKEND_CLASS = backend_factory(selected_backend)['backend_class']

    image = img_label(label)

    # from brother_ql
    qlr = BrotherQLRaster(printer.model)

    create_label(qlr, image, printer.width, threshold=70, cut=True, dither=False, compress=False, red=False)

    try:
        be = BACKEND_CLASS(printer.connection)
        be.write(qlr.data)
        be.dispose()
        del be
    except Exception as e:
        raise NameError(str(e))

    return True
