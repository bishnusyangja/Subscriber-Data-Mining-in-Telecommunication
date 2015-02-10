from django.conf.urls import patterns, include, url
from telde import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'telde.views.home', name='home'),
    # url(r'^telde/', include('telde.foo.urls')),
      url(r'^analysis/',include('analysis.urls',namespace="analysis")),
      url(r'^visualize/',include('visualize.urls',namespace="visualize")),
      url(r'^profiling/',include('profiling.urls',namespace="profiling")),
      
      url(r'^$',views.index,name='home'),      
      # url(r'^about/',views.about,name='about'),
    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
