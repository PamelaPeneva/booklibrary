from rest_framework import generics, permissions, filters
from books.models import Book
from books_api.serializers import BaseBookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BaseBookSerializer

    permission_classes = [permissions.AllowAny]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'genres__name']



