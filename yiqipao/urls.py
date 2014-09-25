from django.conf.urls import patterns, include, url
from yiqipao.settings import *

from django.contrib import admin
admin.autodiscover()

one_mile_patterns = patterns('one_mile.views',
    url(r'^$', 'index'),
    url(r'^index$', 'index'),
    url(r'^login$', 'login'),

    url(r'^logout$', 'logout'),
                             
    url(r'^newuser$', 'reg_page'),
    url(r'^register$', 'register'),

    url(r'^newrun$', 'upload_page'),
    url(r'^upload$', 'upload'),

    url(r'^audit$', 'audit_page'),
    url(r'^audit/detail$', 'audit_detail'),
    url(r'^audit/accept$', 'audit_accept'),
    url(r'^audit/reject$', 'audit_reject'),

    url(r'^profile$', 'profile_page'),
    url(r'^profile/more_log$', 'more_run_log'),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yiqipao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT }),
) + one_mile_patterns
