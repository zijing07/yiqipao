from django.conf.urls import patterns, include, url
from yiqipao.settings import *

from django.contrib import admin
admin.autodiscover()

one_mile_patterns = patterns('one_mile.views',
    url(r'^$', 'index'),
    url(r'^index', 'index'),
    url(r'^login', 'login'),
    url(r'^register', 'register'),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yiqipao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT }),
) + one_mile_patterns
