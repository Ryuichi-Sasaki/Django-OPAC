from django.urls import path

from . import views


app_name = 'opac'
urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('book/<int:pk>/', views.StockListView.as_view(), name='book_detail'),
]
