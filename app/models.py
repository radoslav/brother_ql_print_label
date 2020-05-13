class Printer:
    """
    Custom Printer Class
    """

    def __init__(self, model=None, connection=None, width=None, idVendor=None, idProduct=None):
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

    def __init__(self, id=None, supplier_name=None, print_material_type=None, print_material=None, url=None,
                 copies=None, width=None, grammage_or_height=None):
        self.id = id
        self.supplier_name = supplier_name
        self.print_material_type = print_material_type
        self.print_material = print_material
        self.url = url
        self.copies = copies
        self.width = width
        self.grammage_or_height = grammage_or_height

    def __str__(self):
        return self.id
