from app.models import Label


def jsonToLabel(json):
    label = Label
    label.id = json.get('id')
    label.supplier_name = json.get('supplier_name')
    label.print_material_type = json.get('print_material_type')
    label.print_material = json.get('print_material')
    label.url = json.get('url')
    return label