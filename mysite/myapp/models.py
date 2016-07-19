from django.db import models

class Publisher(models.Model):
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name

class Author(models.Model):
    surname = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    san = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ManyToManyField(Author, through='Authorship', null=True, blank=True)
    publisher = models.ManyToManyField(Publisher, through='Printings', null=True, blank=True)
    name = models.CharField(max_length=500)
    year = models.CharField(max_length=4)
    pages = models.IntegerField(null=True,blank=True)
    tom = models.CharField(max_length=10, null=True, blank = True)
    tom_number = models.CharField(max_length=10, null = True, blank=True)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    udk = models.CharField(max_length=200, null=True, blank=True)
    bbk = models.CharField(max_length=200, null=True, blank=True)
    topics = models.CharField(max_length=500, null=True, blank=True)
    exem = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

class Authorship(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class Printings(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

