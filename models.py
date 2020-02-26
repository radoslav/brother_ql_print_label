class Printer:
    """
    Custom Printer Class
    """

    def __init__(self, model, connection, width, idVendor, idProduct):
        self.model = model
        self.connection = connection
        self.width = width
        self.idVendor = idVendor
        self.idProduct = idProduct

    def __str__(self):
        return self.model


class Label:
    """
    Custom Label Class
    """

    def __init__(self, id, supplier_name, print_material_type, print_material, url):
        self.id = id
        self.supplier_name = supplier_name
        self.print_material_type = print_material_type
        self.print_material = print_material
        self.url = url

    def __str__(self):
        return self.id