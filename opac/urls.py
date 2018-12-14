from django.urls import path

from . import views


app_name = 'opac'
urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('book/<int:book_id>/stocks/',
         views.BookDetailView.as_view(), name='stock_list'),
]
