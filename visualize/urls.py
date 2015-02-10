from django.conf.urls import patterns, url
from visualize import views
urlpatterns=patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^viewing',views.view_type),	
)