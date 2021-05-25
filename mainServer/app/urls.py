from django.urls import path
from .views import BuildingsListView
#ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView


urlpatterns = [
    # 一覧画面
    path('',  BuildingsListView.as_view(), name='index'),
    # 詳細画面
    path('detail/<int:pk>/', BuildingsListView.as_view(), name='detail'),
    # 登録画面
    path('create/', BuildingsListView.as_view(), name='create'),
    # 更新画面
    path('update/<int:pk>/', BuildingsListView.as_view(), name='update'),
    # 削除画面
    path('delete/<int:pk>/', BuildingsListView.as_view(), name='delete'),
]

