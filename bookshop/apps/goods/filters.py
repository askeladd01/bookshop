from django.db.models import Q
from django_filters import rest_framework as filters
from django.utils.translation import ugettext_lazy as _

from .models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    min_price = filters.NumberFilter(field_name="shop_price", lookup_expr='gte', help_text=_('大于等于本店价格'))
    max_price = filters.NumberFilter(field_name="shop_price", lookup_expr='lte', help_text=_('小于等于本店价格'))

    top_category = filters.NumberFilter(field_name="category", method='top_category_filter')

    search_field = filters.CharFilter(field_name='name', lookup_expr='contains')
    ordering = filters.OrderingFilter(fields=('id', 'sold_num', 'shop_price'),
                                      field_labels={'id': '默认', 'sold_num': '销量', 'shop_price': '价格'})

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max']

    @staticmethod
    def top_category_filter(queryset, name, value):
        # 不管当前点击的是一级目录二级目录还是三级目录。
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price', 'is_hot', 'is_new']
