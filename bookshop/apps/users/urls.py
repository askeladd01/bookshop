from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('register', views.RegisterView)
router.register('', views.LoginView, basename='login')
router.register('detail', views.UserView, 'detail')

urlpatterns = [
    path('send_sms/', views.SendSmsView.as_view()),
    path('', include(router.urls)),
]
