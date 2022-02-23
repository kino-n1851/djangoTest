from django.urls import path
from .views import ServerDetailView, ServerListView, ServerAnalyze, ServerCreateView
from .views import ServerUpdateView, ServerDeleteView, RootView, ImageListView
from .views import ImageDetailView, ImageCreateView, ImageUpdateView, ImageDeleteView, ImageAnalyzeView
#ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView


urlpatterns = [
    path('', RootView.as_view(), name="index"),
    # 一覧画面
    path('servers/',  ServerListView.as_view(), name='server_index'),
    # 詳細画面
    path('servers/detail/<int:pk>/', ServerDetailView.as_view(), name='server_detail'),
    path('servers/detail/<int:pk>/analyze/', ServerAnalyze.as_view(), name='server_analyze'),
    # 登録画面
    path('create/', ServerCreateView.as_view(), name='server_create'),
    # 更新画面
    path('update/<int:pk>/', ServerUpdateView.as_view(), name='server_update'),
    # 削除画面
    path('delete/<int:pk>/', ServerDeleteView.as_view(), name='server_delete'),

    path('images/',  ImageListView.as_view(), name='image_index'),
    path('images/detail/<int:pk>/', ImageDetailView.as_view(), name='image_detail'),
    path('images/detail/<int:pk>/analyze/', ImageAnalyzeView.as_view(), name='image_analyze'),
    path('images/create/', ImageCreateView.as_view(), name='image_create'),
    path('images/update/<int:pk>/', ImageUpdateView.as_view(), name='image_update'),
    path('images/delete/<int:pk>/', ImageDeleteView.as_view(), name='image_delete'),

]

