from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mysite.myapp.views.index', name='index'),
    #url(r'^$', 'mysite.myapp.views.publishers', name='publishers'),
    #url(r'^$', 'mysite.myapp.views.results', name='results'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^myapp/', include('mysite.myapp.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
