from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from io import BytesIO
from ftplib import FTP
import base64
import os
import requests
import json
from PIL import Image

def update():
    ftp = FTP("153.127.69.176", "iijimalab00", passwd="island#00")
    items = ftp.nlst(".")
    print(items)
    for item in items:
        if not item.endswith(".png") or item.endswith("_mosaic.png"):
            continue
        filename = item
        print(filename)
        byte = BytesIO()
        ftp.retrbinary('RETR '+ filename, byte.write)
        byte.seek(0)
        img_byte = byte.getvalue()
        img_base64 = base64.b64encode(img_byte)
        img_str = img_base64.decode("utf-8")
        req_img = {
            "img":img_str
        }   
        r = requests.post("http://172.16.20.170:8000/api/mosaic/",
                            json=json.dumps(req_img))

        if True:
            if not 'json' in r.headers.get('content-type'):
                continue
            else:
                json_load = r.json()
                img_str = json_load["img"]
                if img_str is None:
                    print("response is broken.")
                    return
                img = base64.b64decode(img_str)
                img = BytesIO(img)
                img = Image.open(img)
                img.save("updated.png")
                byte = BytesIO()
                img.save(byte, format="png")
                byte.seek(0)
                ftp.delete(filename)
                ftp.storbinary('STOR '+ os.path.splitext(filename)[0] + "_mosaic.png", byte)

    #except Exception as e:
    #    print(e)

def printt():
    print("updated!!")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update, 'interval', minutes=10) # schedule
    scheduler.start()

if __name__ == "__main__":
    update()