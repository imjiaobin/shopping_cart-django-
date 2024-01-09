"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include#抓project內的app
from django.conf.urls.static import static #載入靜態檔案
from django.conf import settings #載入setting,以方便下方建立圖檔的網頁連結

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('store.urls')),#抓store的urls.py的url
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#建立網站內的圖檔網頁連結