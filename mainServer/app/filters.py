from django_filters import filters
from django_filters import FilterSet
from .models import ImageStorage


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = '%s （降順）'

"""
class ItemFilter(FilterSet):

    name = filters.CharFilter(label='氏名', lookup_expr='contains')
    memo = filters.CharFilter(label='備考', lookup_expr='contains')

    order_by = MyOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', 'name'),
            ('age', 'age'),
        ),
        field_labels={
            'name': '氏名',
            'age': '年齢',
        },
        label='並び順'
    )

    class Meta:

        model = Item
        fields = ('name', 'sex', 'memo',)
"""
class StorageFilterSet(FilterSet):
    name = filters.CharFilter(label='サーバ識別名', lookup_expr='contains')
    server_type = filters.CharFilter(label='サーバタイプ', lookup_expr='contains')

    order_by = MyOrderingFilter(
        fields=(
            ('name', 'name'),
            ('server_type', 'server_type'),
        ),
        field_labels={
            'name': 'サーバ識別名',
            'server_type': 'サーバタイプ',
        },
        label='並び順'
    )
    class Meta:
        model = ImageStorage
        fields = ['name', 'server_type']
    
class ImageFilterSet(FilterSet):
    class Meta:
        model = ImageStorage
        fields = ['name']

