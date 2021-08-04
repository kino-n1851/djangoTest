# coding: utf-8
# from rest_framework import routers
from .views import UserViewSet, EntryViewSet, mnist
from django.urls import path
#router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'entries', EntryViewSet)

urlpatterns = [
    path(r'mnist/', mnist),
]