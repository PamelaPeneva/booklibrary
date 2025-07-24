from django.db.models.functions import ExtractYear
from books.models import Book


def get_year_choices():
    years_qs = Book.objects.annotate(year=ExtractYear('published')) \
                           .values_list('year', flat=True) \
                           .distinct()
    years = sorted([y for y in years_qs if y is not None], reverse=True)
    return [('', 'All years')] + [(str(y), str(y)) for y in years]