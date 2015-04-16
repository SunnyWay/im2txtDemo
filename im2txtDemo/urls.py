from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'im2txtDemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^mnlm/', include('mnlm.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
