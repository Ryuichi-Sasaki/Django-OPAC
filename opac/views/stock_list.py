from django.views.generic import ListView

from opac.queries import BookQuery, BookStocksQuery


class StockListView(ListView):
    context_object_name = 'stocks'

    def get_queryset(self):
        return BookStocksQuery(self.kwargs['pk']).query()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = BookQuery(self.kwargs['pk']).query()
        return context
