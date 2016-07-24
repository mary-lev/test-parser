from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
#from django.http import HttpResponse
#from django.views.generic import DetailView
from mysite.myapp.models import Book, Publisher, Author, Authorship, Printings
from collections import Counter
from django import forms
from django.db.models import Q
from mysite.myapp.forms import SearchIsbn
from django.db.models import Count

def index(request):
    all_books = Book.objects.order_by('name')[:10]
    #template = loader.get_template('myapp/index.html')
    #context = RequestContext(request, {        'all_books': all_books,    })
    #return HttpResponse(template.render(context))

    template = "index.html"
    context = { 'all_books': all_books,   }
    return render( request, template, context )

def detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    publisher = book.publisher.all()
    context =  RequestContext(request, { 'book': book, 'publisher': publisher })
    template = 'detail.html'
    return render( request, template, context )

def results(request, publisher_id):
    publisher = Publisher.objects.get(pk=publisher_id)
    books = Book.objects.filter(publisher=publisher_id)
    context =  RequestContext(request, { 'books': books, 'publisher': publisher })
    template = 'results.html'
    return render( request, template, context )

def publishers(request):
    all_publishers = Publisher.objects.order_by('name')
    template = 'publishers.html'
    context = { 'all_publishers': all_publishers,   }
    return render( request, template, context )

def most_publishers(request):
    all_publisher = Publisher.objects.annotate(count_book=Count('book')).order_by('-count_book')[:100]
    template = 'most_publishers.html'
    context = { 'count_publishers': all_publisher,   }
    return render( request, template, context )

def most_authors(request):
    all_books = Author.objects.annotate(count_author=Count('book')).order_by('-count_author')[:100]
    template = 'most_authors.html'
    context = { 'all_books': all_books,   }
    return render( request, template, context )

def authors(request):
    all_authors = Author.objects.order_by('surname')
    template = 'authors.html'
    context = { 'all_authors': all_authors,   }
    return render( request, template, context )

def author(request, author_id):
    a = Author.objects.get(pk=author_id)
    books = Book.objects.filter(author=author_id)
    context =  RequestContext(request, { 'books': books, 'a': a })
    template = 'author.html'
    return render( request, template, context )

def cities(request):
    all_cities1 = Printings.objects.all()
    all_cities = [all.publisher.city for all in all_cities1]
    count_cities = Counter(all_cities).most_common()
    template = 'cities.html'
    context = { 'count_cities': count_cities,   }
    return render( request, template, context )

def city(request, city_name):
    publishers = [p.id for p in Publisher.objects.filter(city=city_name)]
    books = Book.objects.filter(publisher__in=publishers)
    all_b = len(books)
    context =  RequestContext(request, { 'books': books, 'city_name': city_name, 'all_b' : all_b })
    template = 'city.html'
    return render( request, template, context )

def years(request):
    all_years = [all.year for all in Book.objects.all()]
    c = Counter(all_years)
    count_years = c.most_common()
    c = sorted(c.items(), key=lambda i: i[0], reverse=True)
    template = 'years.html'
    context = { 'count_years': count_years, 'c': c }
    return render( request, template, context )

def year(request, one_year):
    books = Book.objects.filter(year=one_year)
    context =  RequestContext(request, { 'books': books, 'one_year' : one_year })
    template = 'year.html'
    return render( request, template, context )

def udks(request):
    all_udk = [all.udk for all in Book.objects.all()]
    all_udk = sorted(set(all_udk))
    context = { 'all_udk': all_udk, }
    return render( request, 'udks.html', context )

def udk(request, one_udk):
    all_books = Book.objects.filter(udk=one_udk)
    context =  RequestContext(request, { 'all_books': all_books, 'one_udk' : one_udk })
    return render( request, 'udk.html', context )

def search_isbn(request):
    if request.method == 'GET':
        form = SearchIsbn(request.GET)
    return render(request, 'search_isbn.html', {'form': form})

def find_isbn(request):
    if request.GET:
        found_entries = Book.objects.filter(isbn=request.GET['isbn'])
    return render(request, 'find_isbn.html',  { 'isbn': request.GET['isbn'], 'books': found_entries },)

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

def most_pages(request):
    books = Book.objects.all().order_by('-pages')
    template = 'most_pages.html'
    return render(request, template, {'books': books[:100]} )

def most_printing(request):
    books = Book.objects.all().order_by('-exem')
    template = 'most_printing.html'
    return render(request, template, {'books': books[:100]} )