#coding: utf-8
from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters

from .models import User, Entry
from .serializer import UserSerializer, EntrySerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import base64
from io import BytesIO
import sys
sys.path.append("/home/keino/YOLOv3")
from keras_yolo3 import *

yolo_args = {   "model_path": '/home/keino/YOLOv3/keras_yolo3/model_data/yolo.h5',
        "anchors_path": '/home/keino/YOLOv3/keras_yolo3/model_data/yolo_anchors.txt',
        "classes_path": '/home/keino/YOLOv3/keras_yolo3/model_data/coco_classes.txt'}
yolo = YOLO_mosaic()

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

@api_view(['GET', 'POST'])
def mnist(request):
    if request.method == 'POST':
        data = request.data
        json_load = json.loads(data)
        img_str = json_load["img"]
        print(json_load["img"])
        img = base64.b64decode(img_str)
        img = BytesIO(img)
        img = Image.open(img)
        img.save("rebuild.png")
        img = np.array(ImageOps.invert(img.convert('L')))
        model = tf.keras.models.load_model('saved_model/model_a',compile=False)
        s = model.predict_classes( img.reshape([1,28,28]) )
        print(s)
        return Response(s[0])
    return Response(-1)

@api_view(['GET', 'POST'])
def  mosaic_YOLO(request):
    global yolo
    if request.method == 'POST':
        data = request.data
        json_load = json.loads(data)
        img_str = json_load["img"]

        img = base64.b64decode(img_str)
        img = BytesIO(img)
        img = Image.open(img)
        img.save("received_YOLO.png")
        r_img = yolo.detect_image(img)
        r_img.save("convert_YOLO.png")
        byte = BytesIO()
        r_img.save(byte, format="png")
        img_byte = byte.getvalue()
        img_base64 = base64.b64encode(img_byte)
        img_str = img_base64.decode("utf-8")
        ret = {
            "img":img_str
        }   
        return JsonResponse(ret)
    return Response(-1)