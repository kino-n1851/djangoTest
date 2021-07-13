from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .models import Building
#from .filters import ItemFilter
#from .forms import ItemForm

from django.shortcuts import render

from PIL import Image
import json
import base64
from io import BytesIO
import requests

# Create your views here.
#LoginRequiredMixin,
class BuildingsListView(FilterView):
    model = Building

    queryset = Building.objects.all().order_by('-name_building')
    print(queryset)
    strict = False
    paginate_by = 10

    def get(self, request, **kwargs):
        print(super().get(request, **kwargs))
        return super().get(request, **kwargs)
"""
class ItemFilterView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    
    queryset = Item.objects.all().order_by('-created_at')
    strict = False
    paginate_by = 10

    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)
"""
# 詳細画面
class BuildingDetailView(LoginRequiredMixin, DetailView):
    model = Building

    
    def get(self, request, **kwargs):
        img = Image.open("./app/test6.png")
        byte = BytesIO()
        img.save(byte, format="png")
        img_byte = byte.getvalue()
        img_base64 = base64.b64encode(img_byte)
        img_str = img_base64.decode("utf-8")
        qqq = {
            "img":img_str
        }   
        entry = {
            "title":"postTest",
            "body":"this body was sent by server",
            "status":"null",
            "author":"keino",
        }
        print(entry)
        print(json.dumps(entry))
        r = requests.post("http://172.16.22.155:8000/api/entries/",json=json.dumps(entry))
        print(r)
        print(r.json())
        return super().get(request, **kwargs)
   

"""

# 登録画面
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


# 削除画面
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('index')
"""