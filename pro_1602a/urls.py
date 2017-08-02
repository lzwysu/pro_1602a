"""pro_1602a URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog import url as blog_url
from django.views.static import serve
from django.conf import settings
from blog.upload import upload_image
from blog.views import acc_login,acc_logout
from qq import urls as qq_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^upload/(.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^admin/upload/(?P<dirname>.+)$',upload_image),
    url(r'^', include(blog_url)),
    url(r'^qq/', include(qq_urls)),
    url(r'^acc_login/$', acc_login ,name='acc_login'),
    url(r'^acc_logout/$', acc_logout ,name='acc_logout'),
]
