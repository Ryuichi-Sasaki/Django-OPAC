from django.views.generic.base import TemplateView


class SearchView(TemplateView):
    template_name = 'opac/search.html'
