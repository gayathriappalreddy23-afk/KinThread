from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category_page, name='category-page'),
    path('search/', views.search_products, name='search-products'),
]
