from django.conf.urls import url,include
from views import *

urlpatterns = [
    url(r'^$', index , name='index'),
    url(r'^category$', category , name='category'),
    url(r'^archive', archive , name='archive'),
    url(r'^tag', tag , name='tag'),
    url(r'^article', article , name='article'),
    url(r'^comment_post/$', comment_post, name='comment_post'),
]
