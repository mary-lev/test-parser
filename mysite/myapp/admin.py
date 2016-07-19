from django.contrib import admin
from mysite.myapp.models import Publisher, Book, Author, Authorship, Printings

class AuthorshipInline(admin.TabularInline):
    model = Authorship
    extra = 1

class PrintingsInline(admin.TabularInline):
    model = Printings
    extra = 1

class PrintingsAdmin(admin.ModelAdmin):
    model = PrintingsInline
    pass

class AuthorshipAdmin(admin.ModelAdmin):
    model = AuthorshipInline
    pass

class BookAdmin(admin.ModelAdmin):
    list_display = ['get_author', 'name', 'year', 'get_publisher', 'pages', 'exem', 'isbn']
    inlines = [AuthorshipInline, PrintingsInline]
    #def publisher_name(self, instance):
    #    return instance.publisher.name
    def get_publisher(self, obj):
        return "\n".join([p.name for p in obj.publisher.all()])
    def get_author(self, obj):
        return "\n".join([' '.join([p.name, p.surname]) for p in obj.author.all()])

class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname']

admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Authorship, AuthorshipAdmin)
admin.site.register(Printings, PrintingsAdmin)