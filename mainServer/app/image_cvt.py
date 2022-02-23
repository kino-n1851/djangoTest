from PIL import Image
from io import BytesIO
import base64

def img_to_str(img):
    byte = BytesIO()
    img.save(byte, format="png") #*png以外未対応
    img_byte = byte.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str

def str_to_img(img_str):
    img = base64.b64decode(img_str)
    img = BytesIO(img)
    img = Image.open(img)
    return img

def byte_to_str(byte):
    img_byte = byte.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    return img_str