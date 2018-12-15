from django.views.generic import ListView

from opac.models.masters import Book
from opac.queries import BookStocksQuery


class StockListView(ListView):
    context_object_name = 'stocks'

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return BookStocksQuery(book_id).query()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['book_id']
        context['book'] = Book.objects.get(pk=book_id)
        return context
