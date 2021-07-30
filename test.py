from PIL import Image
import json
import base64
from io import BytesIO
import requests

img = Image.open("test6.png")
byte = BytesIO()
img.save(byte, format="png")
img_byte = byte.getvalue()
img_base64 = base64.b64encode(img_byte)
img_str = img_base64.decode("utf-8")
print(img_str)
img = base64.b64decode(img_str)
img = BytesIO(img)
img = Image.open(img)
img.save("rebuild.png")
img.show()