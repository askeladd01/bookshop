from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from . import models
from . import serializer
from .filters import GoodsFilter


# Create your views here.

class PageNumPagination(PageNumberPagination):
    """
    分页器
    """
    page_size = 10
    page_query_param = 'page'
    max_page_size = 20
    page_size_query_param = 'page_size'


class BannerView(ListModelMixin, GenericViewSet):
    """
    首页轮播图接口
    """
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('index')[:3]
    serializer_class = serializer.BannerSerializer

    def list(self, request, *args, **kwargs):
        banner_list = cache.get('banner_list')
        if not banner_list:
            response = super(BannerView, self).list(request, *args, **kwargs)
            cache.set('banner_list', response.data, 60 * 60 * 24)
            return response
        return Response(data=banner_list)


class GoodsListViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    商品列表页，分页，过滤，取某一个具体商品的详情
    """
    serializer_class = serializer.GoodsDetailSerializer
    pagination_class = PageNumPagination
    queryset = models.Goods.objects.filter(is_delete=False).order_by('sold_num')

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    ordering_fields = ('id', 'sold_num', 'shop_price')
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        good_serializer = self.get_serializer(instance)
        return Response(good_serializer.data)


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = models.GoodsCategory.objects.all()
    serializer_class = serializer.CategorySerializer


class HotSearchViewSet(ListModelMixin, GenericViewSet):
    """
    热搜词列表
    """
    queryset = models.HotSearchWords.objects.all().order_by("index")
    serializer_class = serializer.HotWordsSerializer


class IndexCategoryViewSet(ListModelMixin, GenericViewSet):
    """
    首页商品分类接口
    """
    queryset = models.IndexAd.objects.filter(is_delete=False)
    serializer_class = serializer.IndexCategorySerializer
