from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
#from django.http import HttpResponse
#from django.views.generic import DetailView
from mysite.myapp.models import Book, Publisher, Author, Authorship, Printings
from collections import Counter, OrderedDict
from django import forms
from django.db.models import Q
from mysite.myapp.forms import SearchIsbn
from django.db.models import Count
import json

def index(request):
    all_books = Book.objects.order_by('name')[:10]
    #template = loader.get_template('myapp/index.html')
    #context = RequestContext(request, {        'all_books': all_books,    })
    #return HttpResponse(template.render(context))

    template = "index.html"
    context = { 'all_books': all_books,   }
    return render( request, template, context )

# карточка книги
def detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    publisher = book.publisher.all()
    context =  RequestContext(request, { 'book': book, 'publisher': publisher })
    template = 'detail.html'
    return render( request, template, context )

# список книг одного издательства
def results(request, publisher_id):
    publisher = Publisher.objects.get(pk=publisher_id)
    books = Book.objects.filter(publisher=publisher_id)
    context =  RequestContext(request, { 'books': books, 'publisher': publisher })
    template = 'results.html'
    return render( request, template, context )

# список всех издательств по алфавиту
def publishers(request):
    all_publishers = Publisher.objects.order_by('name')
    template = 'publishers.html'
    context = { 'all_publishers': all_publishers,   }
    return render( request, template, context )

# самые активные издательства
def most_publishers(request):
    all_publisher = Publisher.objects.annotate(count_book=Count('book')).order_by('-count_book')[:100]
    template = 'most_publishers.html'
    context = { 'count_publishers': all_publisher,   }
    return render( request, template, context )

# самые публикуемые авторы
def most_authors(request):
    all_books = Author.objects.annotate(count_author=Count('book')).order_by('-count_author')[:100]
    template = 'most_authors.html'
    context = { 'all_books': all_books,   }
    return render( request, template, context )

# список всех авторов
def authors(request):
    all_authors = Author.objects.order_by('surname')
    template = 'authors.html'
    context = { 'all_authors': all_authors,   }
    return render( request, template, context )

# список всех книг одного автора
def author(request, author_id):
    a = Author.objects.get(pk=author_id)
    books = Book.objects.filter(author=author_id)
    context =  RequestContext(request, { 'books': books, 'a': a })
    template = 'author.html'
    return render( request, template, context )

# список всех городов
def cities(request):
    all_cities = Publisher.objects.all().values('city').annotate(count_books=Count('book')).order_by('-count_books')
    template = 'cities.html'
    context = { 'count_cities': all_cities,   }
    return render( request, template, context )

# список всех книг, выпущенных в этом городе
def city(request, city_name):
    publishers = [p.id for p in Publisher.objects.filter(city=city_name)]
    books = Book.objects.filter(publisher__in=publishers)
    all_b = len(books)
    context =  RequestContext(request, { 'books': books, 'city_name': city_name, 'all_b' : all_b })
    template = 'city.html'
    return render( request, template, context )

# список всех лет
def years(request):
    all_years = Book.objects.all().values('year').annotate(count_years=Count('year')).order_by('-count_years')
    template = 'years.html'
    context = { 'count_years': all_years }
    return render( request, template, context )

# список всех книг, выпущенных в этом году
def year(request, one_year):
    books = Book.objects.filter(year=one_year)
    context =  RequestContext(request, { 'books': books, 'one_year' : one_year })
    template = 'year.html'
    return render( request, template, context )

# список всех удк
def udks(request):
    all_udk = Book.objects.all().values('udk').annotate(count_udk=Count('udk')).order_by('udk')
    context = { 'all_udk': all_udk, }
    return render( request, 'udks.html', context )

# список всех ббк
def bbks(request):
    all_bbk = Book.objects.all().values('bbk').annotate(count_bbk=Count('bbk')).order_by('bbk')
    context = { 'all_bbk': all_bbk, }
    return render( request, 'bbks.html', context )

# список всех книг по одному ббк
def bbk(request, one_bbk):
    all_books = Book.objects.filter(bbk=one_bbk)
    context =  RequestContext(request, { 'all_books': all_books, 'one_bbk' : one_bbk })
    return render( request, 'bbk.html', context )

# поиск по isbn (форма запроса)
def search_isbn(request):
    if request.method == 'GET':
        form = SearchIsbn(request.GET)
    return render(request, 'search_isbn.html', {'form': form})

# поиск по isbn (ответ)
def find_isbn(request):
    if request.GET:
        found_entries = Book.objects.filter(isbn=request.GET['isbn'])
    return render(request, 'find_isbn.html',  { 'isbn': request.GET['isbn'], 'books': found_entries },)

# поиск дубликатов по isbn
def find_duplicates(request):
    dups = (
    Book.objects.values('isbn')
    .annotate(count=Count('id'))
    .values('isbn')
    .order_by()
    .exclude(isbn='')
    .filter(count__gt=1)
    )
    books = Book.objects.filter(isbn__in=dups).distinct()
    return render( request, 'find_duplicates.html', { 'books': books}, )

# самые толстые книги
def most_pages(request):
    books = Book.objects.all().order_by('-pages')
    template = 'most_pages.html'
    return render(request, template, {'books': books[:100]} )

# самые тиражные книги
def most_printing(request):
    books = Book.objects.all().order_by('-exem')
    template = 'most_printing.html'
    return render(request, template, {'books': books[:100]} )

# список всех городов
def all_cities(request):
    cities = Publisher.objects.all().values('city').order_by('city').distinct().annotate(count_books=Count('id'))
    return render( request, 'all_cities.html', { 'cities': cities, }, )

# издательства в одном городе
def city_publishers(request, one_city):
    publishers = Publisher.objects.filter(city=one_city).order_by('name')
    return render( request, 'city_publishers.html', {'publishers': publishers, 'one_city': one_city}, )

def all_udks(request):
    t = open('/home/bookparser/mysite/mysite/myapp/udks.json', 'r')
    f = t.read()
    data1 = json.loads(f)
    od = OrderedDict(sorted(data1.items()))
    return render( request, 'all_udks.html', {'data1': od}, )

# список всех книг по одному удк
def udk(request, one_udk):
    t = open('/home/bookparser/mysite/mysite/myapp/udks.json', 'r')
    f = t.read()
    data1 = json.loads(f)
    v = data1[one_udk]
    one_udk1 = '[' + one_udk
    all_books = Book.objects.filter(Q(udk__startswith=one_udk) | Q(udk__startswith=one_udk1)).order_by('name')
    context =  RequestContext(request, { 'all_books': all_books, 'one_udk' : one_udk, 'v': v })
    return render( request, 'udk.html', context )