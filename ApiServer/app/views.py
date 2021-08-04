#coding: utf-8
from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters

from .models import User, Entry
from .serializer import UserSerializer, EntrySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import base64
from io import BytesIO

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
