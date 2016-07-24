from django import forms

class SearchIsbn(forms.Form):
    isbn = forms.CharField()
