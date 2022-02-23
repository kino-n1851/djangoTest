from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from io import BytesIO
from ftplib import FTP
import base64
import os
import requests
import json
from PIL import Image
from .image_cvt import byte_to_str, str_to_img
ML_SERVER_IP = "172.16.20.170"
ML_SERVER_PORT = "8000"

class FTPInfo():
    def __init__(self, ip, user, passwd, target=None, processing_type=None):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.target = target
        self.processing_type = processing_type

class Searcher():
    def __init__(self, ftp=None, passwd=None):
        if ftp is not None and passwd is not None:
            self.ftpInfos = [FTPInfo(*ftp, passwd=passwd,)]
        else:
            self.ftpInfos = []
            ftpservers = []
            ftpservers = ImageStorage.objects.filter(server_type="ftp", enable_update=True)
            for f in ftpservers:
                self.ftpInfos.append(FTPInfo(f.ip, f.user_ftp, passwd=f._passwd, target=f.target, processing_type=f.processing_type))

    def update(self):
        for ftpInfo in self.ftpInfos:
            ftp = FTP(ftpInfo.ip, ftpInfo.user, passwd=ftpInfo.passwd)
            items = ftp.nlst(".")
            print(items)
            for item in items:
                if ftpInfo.processing_type == "mosaic_YOLO":
                    if not item.endswith(".png") or item.endswith("_mosaic.png"):
                        continue
                    filename = item
                    print(filename)
                    byte = BytesIO()
                    ftp.retrbinary('RETR '+ filename, byte.write)
                    byte.seek(0)
                    img_str = byte_to_str(byte)
                    req_img = {
                        "img":img_str,
                        "target":ftpInfo.target,
                    }
                    try:
                        r = requests.post("http://{}:{}/api/mosaic/".format(ML_SERVER_IP,ML_SERVER_PORT),
                                            json=json.dumps(req_img),timeout=(3.0, 10.0))
                    except requests.exceptions.RequestException as e:
                        print(e)
                        break

                    if True:
                        if not 'json' in r.headers.get('content-type'):
                            continue
                        else:
                            json_load = r.json()
                            img_str = json_load["img"]
                            if img_str is None:
                                print("response is broken.")
                                continue
                            img = str_to_img(img_str)
                            img.save("updated.png")
                            byte = BytesIO()
                            img.save(byte, format="png")
                            byte.seek(0)
                            ftp.delete(filename)
                            ftp.storbinary('STOR '+ os.path.splitext(filename)[0] + "_mosaic.png", byte)

    def check(self, *args, **kwargs):
        print("update is running.")

    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.check, 'interval', minutes=10) # schedule
        scheduler.start()

if __name__ == "__main__":
    searcher = Searcher(ftp=["153.127.69.176", "iijimalab00"], passwd="island#00")
    searcher.update()
else:
    from .models import ImageStorage