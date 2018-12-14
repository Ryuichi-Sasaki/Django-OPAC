from django.db.models import Q

from opac.models.masters import Book


class BookSearchQuery:
    def __init__(self, words):
        self._words = words

    def query(self):
        queryset = Book.objects.none()
        for word in self._words:
            books = Book.objects \
                .filter(
                    Q(name__icontains=word) |
                    Q(authors__name__icontains=word) |
                    Q(translators__name__icontains=word) |
                    Q(publisher__name__icontains=word)) \
                .distinct()
            queryset = queryset.union(books)
        return queryset.order_by('-publication_date')
