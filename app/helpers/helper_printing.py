import usb.core


def is_printer_on(printer):
    dev = usb.core.find(idVendor=printer.idVendor, idProduct=printer.idProduct)
    if dev:
        return True
    else:
        return False