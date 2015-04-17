from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<im_index>[0-9]+)/$', views.description, name='description'),
	url(r'^diffinitresults/$', views.diffinitresults, name='diffinitresults'),
]
