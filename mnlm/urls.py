from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<im_index>[0-9]+)/$', views.description, name='description'),
	url(r'^diffinitresults/$', views.diffinitresults, name='diffinitresults'),
	url(r'^evaldiffinit/$', views.evaldiffinit, name='evaldiffinit'),
	url(r'^evaldiffinit/(?P<im_index>[0-9]+)/(?P<vote>[0-2])/$', views.evaldiffinitvote, name='evaldiffinitvote'),
	url(r'^upload/$', views.uploaddesc, name='uploaddesc')
]
