from app.models import Label


def jsonToLabels(json):
    labels = []
    for item in json:
        label = Label
        label.id = item.get('id')
        label.supplier_name = item.get('supplier_name')
        label.print_material_type = item.get('print_material_type')
        label.print_material = item.get('print_material')
        label.url = item.get('url')

        labels.append(label)
    return labels
