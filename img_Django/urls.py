"""img_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from myrecord import views
from django.conf.urls import url

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("register/", views.register_request),
                  path('register/homepage/', views.homepage_request),
                  url(r'logout/$', views.logout_request),
                  path('database', views.database_request),
                  url(r'register/img/(?P<op>[1234])$', views.img_process_request),
                  url(r'register/img/\d+/upload', views.upload_img),
url(r'database/delete', views.delete_record)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)