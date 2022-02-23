# coding: utf-8
# from rest_framework import routers
from .views import UserViewSet, EntryViewSet, mnist, mosaic_YOLO
from django.urls import path

urlpatterns = [
    path(r'mnist/', mnist),
    path(r'mosaic/',mosaic_YOLO),
]