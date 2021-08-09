"""bookshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.documentation import include_docs_urls

import xadmin
from xadmin.plugins import xversion
xadmin.autodiscover()
xversion.register_models()


urlpatterns = [
                  path('admin/', xadmin.site.urls),
                  path('user/', include('users.urls')),
                  path('goods/', include('goods.urls')),
                  path('trade/', include('trade.urls')),
                  path('operation/', include('user_operation.urls')),
                  path('docs/', include_docs_urls(title='企鹅书店', authentication_classes=[], permission_classes=[]))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
