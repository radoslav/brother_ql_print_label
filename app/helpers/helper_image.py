import re
from io import BytesIO

import qrcode
from PIL import Image, ImageDraw, ImageFont

def img_label(label):
    width = '      ' if label.width is None else str(label.width)
    grammage = '      ' if label.grammage_or_height is None else str(label.grammage_or_height)

    qr = qrcode.QRCode(box_size=10)
    qr.add_data(label.url)
    qr.make()
    img_qr = qr.make_image()

    fnt = ImageFont.truetype('FreeMonoBold.ttf', 56)
    fnt_2 = ImageFont.truetype('FreeMonoBold.ttf', 60)
    fnt_bigger = ImageFont.truetype('FreeMonoBold.ttf', 76)

    img_txt = Image.new('RGB', (900, 696), color=(255, 255, 255))
    d_offset = 60
    d = ImageDraw.Draw(img_txt)
    d.text((5, d_offset), 'id: ' + str(label.id),
           font=fnt_bigger, fill=(0, 0, 0))
    d.text((10, d_offset + 90), label.supplier_name,
           font=fnt_bigger, fill=(0, 0, 0))
    d.text((10, d_offset + 180), label.print_material_type,
           font=fnt_bigger, fill=(0, 0, 0))
    d.text((10, d_offset + 270), 's: '+width+' g: ' + grammage,
           font=fnt, fill=(0, 0, 0))
    d.text((10, d_offset + 360), re.sub("(.{20})", "\\1\n", label.print_material, 0, re.DOTALL),
           font=fnt, fill=(0, 0, 0))

    img = Image.new('RGB', (696, 1200), color=(255, 255, 255))

    d_id = ImageDraw.Draw(img)
    d_id.text((40, 50), 'ID: ', font=fnt, fill=(0, 0, 0))
    d_id.text((40, 150), str(label.id), font=fnt_2, fill=(0, 0, 0))

    img.paste(img_qr, (300, 0))
    img.paste(img_txt.rotate(-90, expand=1), (0, 400))

    return img

def create_imgs_from_labels(labels):
    imgs = []
    for label in labels:
        img = img_label(label)
        imgs.append(img)
    return imgs

def img_label_2_copies(label):
    img = img_label(label)
    img_2_labels = Image.new('RGB', (696, 2400), color=(255, 255, 255))
    img_2_labels.paste(img, (0, 0))
    img_2_labels.paste(img, (0, 1200))
    return img_2_labels

def img_to_png_bytes(im):
    image_buffer = BytesIO()
    im.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    return image_buffer.read()
