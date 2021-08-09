from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('cart', views.ShoppingCartViewSet, 'cart')
router.register('order', views.OrderViewSet, 'order')

urlpatterns = [
    path('', include(router.urls)),
    path('success/', views.SuccessPayView.as_view())
]