from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Publisher(models.Model):
    city = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Author(models.Model):
    surname = models.CharField(max_length=500)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    san = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.surname

class BBK(models.Model):
    code = models.CharField(max_length=100)
    text = models.CharField(max_length=10000)
    level = models.IntegerField()
    parent = models.CharField(max_length=100, blank=True, null=True)
    sme = models.CharField(max_length=300, blank=True, null=True)
    stat = models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
        return self.code

class BBKnew(models.Model):
    code = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    level = models.IntegerField()
    sme = models.CharField(max_length=300, blank=True, null=True)
    stat = models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
        return self.code

class Book(models.Model):
    author = models.ManyToManyField(Author, through='Authorship', null=True, blank=True)
    publisher = models.ManyToManyField(Publisher, through='Printings', null=True, blank=True)
    name = models.CharField(max_length=500)
    year = models.CharField(max_length=4)
    pages = models.IntegerField(null=True,blank=True)
    tom = models.CharField(max_length=20, null=True, blank = True)
    tom_number = models.CharField(max_length=10, null = True, blank=True)
    isbn = models.CharField(max_length=25, null=True, blank=True)
    udk = models.CharField(max_length=200, null=True, blank=True)
    bbk = models.CharField(max_length=200, null=True, blank=True)
    topics = models.CharField(max_length=500, null=True, blank=True)
    exem = models.IntegerField(null=True, blank=True)
    full = models.CharField(max_length=2000)
    new_bbk = models.ManyToManyField(BBK, through='Bbkship', null=True, blank=True)
    def __str__(self):
        return self.name

class Bbkship(models.Model):
    book = models.ForeignKey(Book)
    bbk = models.ForeignKey(BBK)

class Authorship(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class Printings(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

