from django.contrib import admin

from books.models import Book, Genre


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'all_genres')
    list_filter = ('published',)
    search_fields = ('title', 'author')
    readonly_fields = ('published',)
    filter_horizontal = ('genres',)

    def all_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    all_genres.short_description = 'Genres'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
