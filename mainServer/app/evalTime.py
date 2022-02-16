import requests
import glob
import time
from PIL import Image 
from io import BytesIO
import base64
import json
import argparse

def main()->None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()

    test_img = Image.open("./machi2.jpg")
    byte = BytesIO()
    test_img.save(byte, format="png")
    img_byte = byte.getvalue()
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode("utf-8")
    req_img = {
        "img":img_str,
        "target":"person"
    }   
    r = requests.post("http://172.16.20.170:8000/api/mosaic/",json=json.dumps(req_img))

    paths_img = glob.glob("./{}/*.png".format(args.dir))
    #print(paths_img)
    imgs_str = []
    for path in paths_img:
        img = Image.open(path)
        byte = BytesIO()
        img.save(byte, format="png")
        img_byte = byte.getvalue()
        img_base64 = base64.b64encode(img_byte)
        img_str = img_base64.decode("utf-8")
        imgs_str.append(img_str)
    num = len(imgs_str)
    print("{} images were found.".format(num))
    time_b = time.perf_counter()
    for img in imgs_str:
        req_img = {
            "img":img_str,
            "target":"person"
        }   
        r = requests.post("http://172.16.20.170:8000/api/mosaic/",json=json.dumps(req_img))
    time_a = time.perf_counter()
    print("{} seconds passed in processing {} images.".format(time_a - time_b, num))
    print("The processing time per image is {} seconds.".format((time_a - time_b)/num))
    
if __name__ == "__main__":
    main()