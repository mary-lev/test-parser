from django.conf.urls import patterns, url

from mysite.myapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^publishers', views.publishers, name='publishers'),
    url(r'^most_publishers', views.most_publishers, name='most_publishers'),
    url(r'^authors', views.authors, name='authors'),
    url(r'^most_authors', views.most_authors, name='most_authors'),
    url(r'^cities', views.cities, name='cities'),
    url(r'^years', views.years, name='years'),
    url(r'^udks', views.udks, name='udks'),
    url(r'^most_pages', views.most_pages, name='most_pages'),
    url(r'^most_printing', views.most_printing, name='most_printing'),
    url(r'^search_isbn', views.search_isbn, name='search_isbn'),
    url(r'^find_isbn', views.find_isbn, name='find_isbn'),
    url(r'^find_duplicates', views.find_duplicates, name='find_duplicates'),
    # book
    url(r'^(?P<book_id>\d+)/$', views.detail, name='detail'),
    # publisher: ex: /polls/5/results/
    url(r'^(?P<publisher_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<author_id>\d+)/author/$', views.author, name='author'),
    # ex: /polls/5/vote/
    url(r'^(?P<city_name>.*)/city/$', views.city, name='city'),
    url(r'^(?P<one_year>.*)/year/$', views.year, name='year'),
    url(r'^(?P<one_udk>.*)/udk/$', views.udk, name='udk'),
    #url(r'^find_isbn/?isbn=(?P<isbn>.*)$', views.find_isbn, name='find_isbn'),
)