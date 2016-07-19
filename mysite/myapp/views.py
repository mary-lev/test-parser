from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.generic import DetailView
from mysite.myapp.models import Book, Publisher, Author, Authorship, Printings

def index(request):
    all_books = Book.objects.order_by('name')
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


def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)

