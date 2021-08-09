from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('banner', views.BannerView, 'banner')
router.register('list', views.GoodsListViewSet, 'list')
router.register('category', views.CategoryViewSet, 'category')
router.register('hotsearch', views.HotSearchViewSet, 'hotsearch')
router.register('indexgoods', views.IndexCategoryViewSet, 'indexgoods')
urlpatterns = [
    path('', include(router.urls))
]