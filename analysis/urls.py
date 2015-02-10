from django.conf.urls import patterns, url
from analysis import views
urlpatterns=patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^sample',views.filter),	
)