from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('favs', views.UserFavViewSet, 'user_favs')
router.register('msg', views.LeavingMessageViewSet, 'user_msg')
router.register('address', views.AddressViewSet, 'user_address')

urlpatterns = [
    path('', include(router.urls)),
]