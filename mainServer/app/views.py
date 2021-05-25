from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .models import Building
#from .filters import ItemFilter
#from .forms import ItemForm

from django.shortcuts import render

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

# 詳細画面
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


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