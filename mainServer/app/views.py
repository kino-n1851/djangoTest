from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .models import ImageStorage, NumberImage
from .filters import StorageFilterSet, ImageFilterSet
from .forms import StorageForm, ImageForm

from django.shortcuts import render

from PIL import Image
import json
import base64
from io import BytesIO
import requests
from .image_cvt import img_to_str, str_to_img
from .search import Searcher
import os

# Create your views here.
#リスト画面
class ServerListView(FilterView):
    model = ImageStorage

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

    # django-filter 設定
    filterset_class = StorageFilterSet
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get_queryset(self):
        return ImageStorage.objects.all().order_by('-name')

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['ImageStorage_list'] = self.get_queryset()
        return super().get_context_data(object_list=object_list, **kwargs)

# 詳細画面
class ServerDetailView(LoginRequiredMixin, DetailView):
    model = ImageStorage
    tamplate_name = 'imagestorage_detail.html'

class ServerAnalyze(LoginRequiredMixin, DetailView):
    model = ImageStorage
    tamplate_name = 'imagestorage_detail.html'
    
    def get(self, request, pk, **kwargs):
        server = ImageStorage.objects.get(pk=pk)
        if server.server_type == "ftp":
            searcher = Searcher(ftp=[server.ip, server.user_ftp], passwd=server._passwd)
            print([server.ip, server.user_ftp])
            #searcher.update()
        else:
            print("serverType is {}.".format(server.server_type))
        return super().get(request, pk, **kwargs)
        

# 登録画面
class ServerCreateView(LoginRequiredMixin, CreateView):
    model = ImageStorage
    form_class = StorageForm
    success_url = reverse_lazy('server_index')

class ServerUpdateView(LoginRequiredMixin, UpdateView):
    model = ImageStorage
    form_class = StorageForm
    success_url = reverse_lazy('server_index')

class ServerDeleteView(LoginRequiredMixin, DeleteView):
    model = ImageStorage
    success_url = reverse_lazy('server_index')

class RootView(TemplateView):
    template_name = 'app/index.html'


class ImageListView(FilterView):
    model = NumberImage

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

    # django-filter 設定
    filterset_class = ImageFilterSet
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get_queryset(self):
        return NumberImage.objects.all().order_by('-imageName')

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['numberimage_list'] = self.get_queryset()
        return super().get_context_data(object_list=object_list, **kwargs)

class ImageDetailView(LoginRequiredMixin, DetailView):
    model = NumberImage
    tamplate_name = 'numberimage_detail.html'

class ImageCreateView(LoginRequiredMixin, CreateView):
    model = NumberImage
    form_class = ImageForm
    success_url = reverse_lazy('image_index')

class ImageUpdateView(LoginRequiredMixin, UpdateView):
    model = NumberImage
    form_class = ImageForm
    success_url = reverse_lazy('image_index')

class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = NumberImage
    success_url = reverse_lazy('image_index')

class ImageAnalyzeView(LoginRequiredMixin, DetailView):
    model = NumberImage
    tamplate_name = 'imagestorage_detail.html'

    def get(self, request, pk, **kwargs):
        savedImage = NumberImage.objects.get(pk=pk)
        print(os.getcwd())
        img = Image.open("./media/{}".format(savedImage.image))
        img_str = img_to_str(img)
        req_img = {
            "img":img_str,
        }   
        #r = requests.post("http://172.16.20.170:8000/api/mnist/",json=json.dumps(req_img))
        print("mnist is running.")
        r=[2]
        savedImage.number = r[0]
        savedImage.save()
        return super().get(request, **kwargs)
