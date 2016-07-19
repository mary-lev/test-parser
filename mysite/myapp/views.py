from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from mysite.myapp.models import Book

def index(request):
    from django import forms
    all_books = Book.objects.order_by('name')
    #template = loader.get_template('myapp/index.html')
    #context = RequestContext(request, {        'all_books': all_books,    })
    #return HttpResponse(template.render(context))
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)

    template = "index.html"
    context = { "form" : NameForm(), 'all_books': all_books,   }
    return render( request, template, context )

def detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    template = loader.get_template('myapp/detail.html')
    context = RequestContext(request, {
        'book': book,
    })
    return HttpResponse(template.render(context))

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)
