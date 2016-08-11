from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
#from django.http import HttpResponse
#from django.views.generic import DetailView
from mysite.myapp.models import Book, Publisher, Author, Authorship, Printings, BBK
from collections import Counter, OrderedDict
from django import forms
from django.db.models import Q
from mysite.myapp.forms import SearchIsbn
from django.db.models import Count
import json
import csv

class Udc():
    def __init__(self, text):
        self.text = text
        self.children = []

    def add_next(self, code):
        #assert isinstance(node, Tree)
        self.children.append(code)

    def find_level(self):
        stop = [':', '#', '(', '$', '->', '/']
        if not any(l in self.text for l in stop):
            split_code = self.text.split(' ')
            new_split = split_code[0].split('.')
            t = 0
            for all in new_split:
                t = t + len(all)
        else:
            t = 'None'
        return t

def try_udk(request):
    with open('/home/bookparser/files/udk_test1.txt', 'r') as f:
        text = f.readlines()

    test = {}
    second = {}
    first = ''
    third = []
    for all in text:
        if not all.startswith('->') and not all.startswith('#') and not all.startswith('->') and '$' not in all:
            new = all.split(' ')
            if ':' not in new[0] and '-' not in new[0]:
                numb = new[0].split('.')
                if len(numb)==1:
                    second = OrderedDict(sorted(second.items()))
                    test[first] = second
                    first = all
                    second = {}
                elif len(numb)==2:
                    if len(third)>0:
                        second[all] = third
                        third = []
                    else:
                        second[all] = []
                else:
                    third.append(all)
    test = OrderedDict(sorted(test.items()))
    udk = []
    for all in text:
        udk.append (Udc(all))
    return render( request, 'try_udk.html', {'test': test, 'udk': udk}, )

def try_bbk(request):
    bbk = BBK.objects.filter(Q(level=1)|Q(level=2))
    return render (request, 'try_bbk.html', {'bbk': bbk}, )

def the_bbk(request, bbk):
    b = BBK.objects.filter(code=bbk)
    bbk = "ББК " + bbk
    books = Book.objects.filter(bbk__startswith=bbk)
    return render(request, 'the_bbk.html', {'books': books, 'bbk': bbk, 'b': b}, )
